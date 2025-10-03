package com.example.sleep_application.database.dao;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import com.example.sleep_application.database.entity.UserEntity;

import java.util.List;

@Dao
public interface UserDao {
    @Query("SELECT * FROM userentity")
    List<UserEntity> getAll();

    @Query("SELECT count(*) != 0 FROM userentity AS p WHERE p.email = :email")
    boolean findPrimaryKeyExists(String email);

    @Query("SELECT username, email FROM userentity AS p WHERE p.email = :email")
    UserEntity findUser(String email);

    @Insert
    void insertAll(UserEntity... userEntities);

    @Delete
    void delete(UserEntity userEntity);
}
