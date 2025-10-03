{-# OPTIONS_GHC -Wno-missing-export-lists #-}

-- code by 32868901 Yin Lam Lo



--This module contains the skeleton code for the assignment.
--
-- Please do not change the names of the parseExerciseX functions, as they
-- are used by the test suite.
--
-- You may, and are highly encouraged, to create your functions.
module Assignment where

import Instances
import Parser
import Control.Applicative

import Data.List (intercalate)

data ADT
  = Empty
  | JSInteger Int
  | JSString String
  | JSArray [ADT]
  | JSTrue
  | JSFalse
  | JSNull
  | Operation ADT [Char] ADT
  | Bracket ADT
  | Not ADT
  | Ternary ADT ADT ADT
  | JSConst ADT ADT      -- constName ADT
  | Chunk [ADT]
  | JSFuncCall ADT [ADT] -- funcName param
  | Braces ADT
  | JSSpace String
  | JSReturn ADT
  | JSFunction ADT [ADT] ADT  -- funcName param statements
  | JSIf ADT ADT
  | JSElse ADT ADT
  | JSVar String
  | JSTail ADT [ADT] [ADT] [ADT]
  deriving (Eq)

instance Show ADT where
  show :: ADT -> String
  show Empty = "You must write a pretty printer!"
  show (JSInteger number) = show number
  show (JSString str) = show str
  show (JSArray value) = "[" ++ intercalate ", " (fmap show value) ++ "]"
  show JSTrue = "true"
  show JSFalse = "false"
  show JSNull = "null"
  show (Operation v1 symbol v2) = show v1 ++ " " ++ symbol ++ " " ++ show v2
  show (Bracket vexpr) = "(" ++ show vexpr ++ ")"
  show (Not bool) = "!" ++ show bool
  show (Ternary condition v1 v2) = show condition ++ " ? " ++ show v1 ++ " : " ++ show v2
  show (JSConst varName value) = "const " ++ show varName ++ " = " ++ show value ++ ";"
  show (Chunk stmt) = intercalate " " (fmap show stmt)
  show (JSFuncCall funcName condition) = show funcName ++ "(" ++  intercalate ", " (fmap show condition)  ++ ")"
  show (Braces content) = "{" ++ show content ++ "}"
  show (JSSpace temp) = " "
  show (JSReturn value) = "return " ++ show value ++ ";"
  show (JSFunction funcName param chunk) = "function " ++ show funcName ++ "(" ++ intercalate ", " (fmap show param) ++ ") " ++ show chunk
  show (JSIf condition chunk) = "if ( " ++ show condition ++ " ) " ++ show chunk
  show (JSElse if_ chunk) = show if_ ++ " else " ++ show chunk
  show (JSVar str) = str
  show (JSTail funcName param chunk tailReturn) = "function " ++ show funcName ++ "(" ++ intercalate ", " (fmap show param) ++ ") {\n\twhile (true) {\n\t\t" ++ intercalate "\n\t\t" (fmap show chunk) ++ "\n\t\t[" ++ intercalate ", " (fmap show param) ++ "] = [" ++ intercalate ", " (fmap show tailReturn) ++ "];\n\t}\n}" 

isTok :: Char -> Parser Char
isTok c = tok (is c)

expr :: Parser ADT
expr = bracket <|> jsInteger <|> jsString <|> jsBool <|> jsNull <|> list <|> jsNot

statement :: Parser ADT
statement = braces <|> statements <|> function <|> jsElse <|> jsIf <|> expr 

jsInteger :: Parser ADT
jsInteger = fmap JSInteger int

jsTrue :: Parser ADT
jsTrue = JSTrue <$ string "true"

jsFalse :: Parser ADT
jsFalse = JSFalse <$ string "false"

jsBool :: Parser ADT
jsBool = jsTrue <|> jsFalse

jsNull :: Parser ADT
jsNull = JSNull <$ string "null"

quoteString :: Parser String
quoteString = is '"' *> many (isNot '"') <* is '"'

jsString :: Parser ADT
jsString = fmap JSString (spaces *> quoteString)

bracket :: Parser ADT -- ternary and jsOperation is here because of its belongs to expr it cause loop 
bracket = fmap Bracket (isTok '(' *> (ternary <|> jsOperation <|> expr) <* spaces <* isTok ')')

jsNot :: Parser ADT
jsNot = fmap Not (isTok '!' *> expr)

jsVar :: Parser ADT
jsVar = fmap JSVar (some (alpha <|> digit <|> is '_'))

operationSymbol :: Parser [Char]
operationSymbol = stringTok "&&" <|> stringTok "||" <|> stringTok "**" <|>
              stringTok "+" <|> stringTok "-" <|> stringTok "*" <|> stringTok "/"
              <|> stringTok "===" <|> stringTok "!==" <|> stringTok ">" <|> stringTok "<"   

jsOperation :: Parser ADT
jsOperation = fmap Operation
              ((funcCall <|> expr <|> jsVar) <* spaces) <*> operationSymbol <*> (spaces *> (funcCall <|> bracket <|> expr <|> jsVar))

ternary :: Parser ADT
ternary = fmap Ternary
          (expr <* spaces <* isTok '?') <*>
          (expr <* spaces) <*>
          (isTok ':' *> expr)

braces :: Parser ADT
braces = fmap Braces (isTok '{' *> (statements <|> jsSpace) <* isTok '}')

jsSpace :: Parser ADT   -- Parser String convert to Parser ADT
jsSpace = JSTrue <$ string "true"

jsConst :: Parser ADT     -- const _ = _ ;
jsConst = fmap JSConst
          ( stringTok "const" *> jsVar <* spaces <* isTok '=') <*> -- const name
          ( (expr <|> funcCall) <* spaces <* isTok ';' <* spaces)

statements :: Parser ADT
statements = fmap Chunk (some (jsConst <|> jsReturn <|> jsElse <|> jsIf) <* spaces)

sepBy1 :: Parser a -> Parser b -> Parser [a]
sepBy1 x y = liftA2 (:) x (many $ y *> x)
sepBy :: Parser a -> Parser b -> Parser [a]
sepBy x y = sepBy1 x y <|> pure []

list :: Parser ADT
list = fmap JSArray (is '[' *> sepBy expr commaTok <* is ']')

funcCall :: Parser ADT
funcCall = fmap JSFuncCall
           jsVar <* isTok '(' <*> -- func name
           sepBy (expr <|> jsVar) commaTok <* isTok ')' -- param




jsIf :: Parser ADT
jsIf = fmap JSIf (stringTok "if" *> isTok '(' *> (bracket <|> ternary <|> jsOperation) <* spaces <* isTok ')') <*> braces

jsElse :: Parser ADT
jsElse = fmap JSElse jsIf <*> (spaces *> stringTok "else" *> braces)

jsReturn :: Parser ADT
jsReturn = fmap JSReturn (stringTok "return" *> (bracket <|> funcCall <|> jsVar) <* isTok ';')

function :: Parser ADT
function = fmap JSFunction
       ( stringTok "function" *> jsVar) <*> -- funcName
       ( isTok '(' *> sepBy jsVar commaTok <* isTok ')') <*> -- param
       braces


jsTail :: Parser ADT
jsTail = fmap JSTail 
       (stringTok "function" *> jsVar) <*> -- funcName
       (isTok '(' *> sepBy jsVar commaTok <* isTok ')' <* isTok '{') <*> -- param
       (some jsIf <* spaces) <*> -- if if if
       (stringTok "return" *> jsVar *> isTok '(' *> -- <*> -- func name
       (sepBy (expr <|> jsVar) commaTok <* isTok ')' <* isTok ';')) -- rtn value




-- | Exercise A

parseExerciseA :: Parser ADT
parseExerciseA = statement

prettyPrintExerciseA :: ADT -> String
prettyPrintExerciseA = show

-- | Exercise B

parseExerciseB :: Parser ADT
parseExerciseB = statement

prettyPrintExerciseB :: ADT -> String
prettyPrintExerciseB = show

-- | Exercise C

-- This function should determine if the given code is a tail recursive function
isTailRecursive :: String -> Bool
isTailRecursive str = case parse jsTail str of  -- if it could successfully parse a jsTail
  Error _ -> False
  Result _ _ -> True

parseExerciseC :: Parser ADT
parseExerciseC = jsTail <|> statement 
-- either it parsed as a jsTail or parsed normally, "show" for jsTali and statement are different

prettyPrintExerciseC :: ADT -> String
prettyPrintExerciseC = show