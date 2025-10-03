package com.example.sleep_application.database.entity;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

import java.time.LocalDate;

@Entity
public class DayEntity {
    @PrimaryKey
    LocalDate date;
}
