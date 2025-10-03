package com.example.sleep_application.database.dao;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import com.example.sleep_application.database.entity.SleepEntity;

import java.util.List;

@Dao
public interface SleepDao {
    @Query("SELECT * FROM sleepentity")
    List<SleepEntity> getAll();

    @Query("SELECT * FROM sleepentity where email = :email")
    List<SleepEntity> getAllByUser(String email);

    @Insert
    void insertAll(SleepEntity... sleepEntities);

    @Delete
    void delete(SleepEntity sleepEntity);
}
