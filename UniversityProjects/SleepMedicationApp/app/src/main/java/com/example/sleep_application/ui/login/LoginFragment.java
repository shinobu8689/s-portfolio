package com.example.sleep_application.ui.login;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.room.Room;

import com.example.sleep_application.database.LocalSqlDbService;
import com.example.sleep_application.database.entity.UserEntity;
import com.example.sleep_application.databinding.FragmentLoginBinding;
import com.google.android.material.snackbar.Snackbar;

public class LoginFragment extends Fragment {

    private FragmentLoginBinding binding;
    LocalSqlDbService dbService;



    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        LoginViewModel loginViewModel =
                new ViewModelProvider(this).get(LoginViewModel.class);

        binding = FragmentLoginBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textLogin;
        loginViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        binding.loginButton.setOnClickListener(this::onClickLogin);
        binding.newAccButton.setOnClickListener(this::onClickNewAcc);

        dbService = Room.databaseBuilder(requireActivity().getApplicationContext(), LocalSqlDbService.class, "appUserDb")
                .allowMainThreadQueries().build();

        return root;
    }

    public void onClickLogin(View view) {

        // log current user in DB for debugging
        Log.d("LoginFragment", dbService.userDao().getAll().toString());

        String username = binding.inputUsername.getText().toString();
        String email = binding.inputEmail.getText().toString();

        if (profileConditionCheck(username, email)) {
            // if the database have email record
            if (dbService.userDao().findPrimaryKeyExists(email) && dbService.userDao().findUser(email).getUsername().equals(username)) {

                // set logged in user as current user
                SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPref.edit();
                editor.putString("login_username", username);
                editor.putString("login_email", email);
                editor.apply();
                Snackbar.make(view, new StringBuffer("Login Success!"), Snackbar.LENGTH_SHORT).show();
            } else {
                Snackbar.make(view, new StringBuffer("Username and Email does not match."), Snackbar.LENGTH_SHORT).show();
            }
        }
    }

    public void onClickNewAcc(View view) {
        String username = binding.inputUsername.getText().toString();
        String email = binding.inputEmail.getText().toString();

        // user name must not be empty and email must be in format
        if (this.profileConditionCheck(username, email)) {
            // and email must not exist in database -> create new acc, else do nothing
            if (!dbService.userDao().findPrimaryKeyExists(email)){

                // create new user into DB
                UserEntity userEntity = new UserEntity(username, email);
                dbService.userDao().insertAll(userEntity);
                Snackbar.make(view, new StringBuffer("User created."), Snackbar.LENGTH_SHORT).show();

                // put created user into sharedPref
                SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPref.edit();
                editor.putString("login_username", username);
                editor.putString("login_email", email);
                editor.apply();

            } else {
                Snackbar.make(view, new StringBuffer("Email already Exist. Please Login."), Snackbar.LENGTH_SHORT).show();
            }
        } else {
            // failed input format
            Snackbar.make(view, new StringBuffer("Invalid Email."), Snackbar.LENGTH_SHORT).show();
        }
    }

    private Boolean profileConditionCheck(String username, String email) {
        //regex checking
        return username.matches("\\w+") && email.matches("^[\\w-.]+@([\\w-]+\\.)+[\\w-]{2,4}$");
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}