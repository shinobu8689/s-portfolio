package com.example.sleep_application.ui.manual_log;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.TimePicker;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.room.Room;

import com.example.sleep_application.R;
import com.example.sleep_application.database.LocalSqlDbService;
import com.example.sleep_application.database.entity.SleepEntity;
import com.google.android.material.snackbar.Snackbar;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.Locale;

public class ManualLogFragment extends Fragment {

    int hour, minute, month, day;
    private com.example.sleep_application.databinding.FragmentManualLogBinding binding;


    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        ManualLogViewModel manualLogView =
                new ViewModelProvider(this).get(ManualLogViewModel.class);

        binding = com.example.sleep_application.databinding.FragmentManualLogBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        Button startButton = root.findViewById(R.id.manual_log_start);

        month = LocalDate.now().getMonthValue();
        day = LocalDate.now().getDayOfMonth();
        startButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                popTimePicker(view, binding.manualLogStartTime);
            }
        });

        Button endButton = root.findViewById(R.id.manual_log_end);
        endButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                popTimePicker(view, binding.manualLogEndTime);
            }
        });

        binding.manualLogDateBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                popDatePicker(view, binding.manualLogDate);
            }
        });

        Button saveButton = root.findViewById((R.id.manual_log_save));
        saveButton.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                saveData(view);
            }
        }));

        final TextView textView = binding.textManualLog;

        manualLogView.getText().observe(getViewLifecycleOwner(), textView::setText);


        return root;
    }

    public void popTimePicker(View view, TextView time) {
        TimePickerDialog.OnTimeSetListener onTimeSetListener = (timePicker, selectedHour, selectedMinute) -> {
            hour = selectedHour;
            minute = selectedMinute;
            time.setText(String.format(Locale.getDefault(), "%02d:%02d", hour, minute));
        };

        int style = AlertDialog.BUTTON_NEGATIVE;
        // The themeResId is the ID that gives us the "spinner style" choice of time
        TimePickerDialog timePickerDialog = new TimePickerDialog(this.getContext(), 16973939, onTimeSetListener, hour, minute, true);
        timePickerDialog.setTitle("Select Time");
        timePickerDialog.show();
    }

    public void popDatePicker(View view, TextView date) {
        DatePickerDialog.OnDateSetListener onDateSetListener = (datePicker, year, month, day) -> {
            this.month = month;
            this.day = day;
            date.setText(String.format(Locale.getDefault(), "%d/%d", month, day));
        };

        int style = AlertDialog.BUTTON_NEGATIVE;
        // The themeResId is the ID that gives us the "spinner style" choice of time
        DatePickerDialog datePickerDialog = new DatePickerDialog(this.getContext(), 16973939, onDateSetListener, LocalDate.now().getYear(), month, day);
        datePickerDialog.setTitle("Select Date");
        datePickerDialog.show();
    }

    public void saveData(View view) {

        SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
        String email = sharedPref.getString("login_email", "No email");

        LocalTime endTime = LocalTime.parse(binding.manualLogEndTime.getText());
        LocalTime startTime = LocalTime.parse(binding.manualLogStartTime.getText());

        LocalDateTime endDateTime = LocalDateTime.of(LocalDate.now(), endTime);
        LocalDateTime startDateTime;

        if (startTime.isAfter(endTime)) {
            startDateTime = LocalDateTime.of(LocalDate.now().minusDays(1), startTime);
        } else {
            startDateTime = LocalDateTime.of(LocalDate.now(), startTime);
        }

        long seconds = Duration.between(startDateTime, endDateTime).toMillis() / 1000;

        SleepEntity sleepEntity = new SleepEntity(email, LocalDate.of(LocalDate.now().getYear(), month, day), endTime, seconds);

        Room.databaseBuilder(requireActivity().getApplicationContext(), LocalSqlDbService.class, "appDb")
                .allowMainThreadQueries().build().sleepDao().insertAll(sleepEntity);


        Snackbar.make(view, new StringBuffer("Sleep Saved"), Snackbar.LENGTH_SHORT).show();
    }


}
