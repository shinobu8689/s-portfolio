package com.example.sleep_application.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

import org.jetbrains.annotations.NotNull;

@Entity
public class UserEntity {

    @NotNull
    @ColumnInfo(name = "username")
    String username;

    @PrimaryKey
    @NotNull
    @ColumnInfo(name = "email")
    String email;

    public UserEntity(@NotNull String username, @NotNull String email) {
        this.username = username;
        this.email = email;
    }

    @NotNull
    public String getUsername() {
        return username;
    }

    public void setUsername(@NotNull String username) {
        this.username = username;
    }

    @NotNull
    public String getEmail() {
        return email;
    }

    public void setEmail(@NotNull String email) {
        this.email = email;
    }

    @Override
    @NotNull
    public String toString() {
        return this.username + " | " + this.email;
    }

}
