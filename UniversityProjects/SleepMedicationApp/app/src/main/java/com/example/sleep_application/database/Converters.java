package com.example.sleep_application.database;

import androidx.room.TypeConverter;


import java.time.LocalDate;
import java.time.LocalTime;

public class Converters {

    @TypeConverter
    public static LocalDate LocalDateFromString(String value) {
        return value == null ? null : LocalDate.parse(value);
    }

    @TypeConverter
    public static String LocalDateToString(LocalDate date) {
        return date == null ? null : date.toString();
    }

    @TypeConverter
    public static LocalTime LocalTimeFromString(String value) {
        return value == null ? null : LocalTime.parse(value);
    }

    @TypeConverter
    public static String LocalTimeToString(LocalTime localTime) {
        return localTime == null ? null : localTime.toString();
    }
}
