package com.example.sleep_application.ui.sleep_tracking_timer;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
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
import com.example.sleep_application.database.entity.SleepEntity;
import com.example.sleep_application.databinding.FragmentSleepTrackingBinding;
import com.google.android.material.snackbar.Snackbar;

import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Locale;

public class SleepTrackingFragment extends Fragment {

    // Number of seconds displayed
    // on the stopwatch.
    private int seconds = 0;

    // Is the stopwatch running?
    private boolean running;

    private boolean wasRunning;

    private long stopTime = Instant.now().getEpochSecond();

    private FragmentSleepTrackingBinding binding;

    LocalSqlDbService dbService;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        SleepTrackingViewModel sleepTrackingViewModel =
                new ViewModelProvider(this).get(SleepTrackingViewModel.class);

        binding = FragmentSleepTrackingBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.timeView;
        sleepTrackingViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        if (savedInstanceState != null) {

            // Get the previous state of the stopwatch
            // if the activity has been
            // destroyed and recreated.
            seconds
                    = savedInstanceState
                    .getInt("seconds");

            stopTime = savedInstanceState.getLong("stopTime");

            running
                    = savedInstanceState
                    .getBoolean("running");
            wasRunning
                    = savedInstanceState
                    .getBoolean("wasRunning");
        }

        if (wasRunning) seconds += Instant.now().getEpochSecond() - stopTime;

        refreshTimer();

        binding.startButton.setOnClickListener(this::onClickStart);

        binding.stopButton.setOnClickListener(this::onClickStop);

        binding.resetButton.setOnClickListener(this::onClickReset);

        binding.saveBtn.setOnClickListener(this::onClickSave);

        runTimer();

        dbService = Room.databaseBuilder(requireActivity().getApplicationContext(), LocalSqlDbService.class, "appDb")
                .allowMainThreadQueries().build();

        return root;
    }

    // Save the state of the stopwatch
    // if it's about to be destroyed.
    @Override
    public void onSaveInstanceState(
            Bundle savedInstanceState)
    {
        savedInstanceState
                .putInt("seconds", seconds);
        savedInstanceState
                .putBoolean("running", running);
        savedInstanceState
                .putBoolean("wasRunning", wasRunning);
        savedInstanceState
                .putLong("stopTime", Instant.now().getEpochSecond());
    }

    public void onClickSave(View view) {

        // TODO : condition to check not logged in?
        SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
        String email = sharedPref.getString("login_email", "No email");

        SleepEntity sleepEntity = new SleepEntity(email, LocalDate.now(), LocalTime.now(), seconds);
        Log.d("SleepEntity", sleepEntity.toString());
        dbService.sleepDao().insertAll(sleepEntity);

        Snackbar.make(view, new StringBuffer("Sleep Saved"), Snackbar.LENGTH_SHORT).show();

        seconds = 0;

        Log.d("SleepEntityDB", dbService.sleepDao().getAll().toString());
        view.setVisibility(View.INVISIBLE);
    }

    // Start the stopwatch running
    // when the Start SaveBtn is clicked.
    // Below method gets called
    // when the Start SaveBtn is clicked.
    public void onClickStart(View view)
    {
        running = true;
    }

    // Stop the stopwatch running
    // when the Stop SaveBtn is clicked.
    // Below method gets called
    // when the Stop SaveBtn is clicked.
    public void onClickStop(View view)
    {
        if (seconds > 0) {
            binding.saveBtn.setVisibility(View.VISIBLE);
        }
        running = false;
    }

    // Reset the stopwatch when
    // the Reset SaveBtn is clicked.
    // Below method gets called
    // when the Reset SaveBtn is clicked.
    public void onClickReset(View view)
    {
        running = false;
        seconds = 0;
    }

    // Sets the NUmber of seconds on the timer.
    // The runTimer() method uses a Handler
    // to increment the seconds and
    // update the text view.
    private void runTimer()
    {
        // Creates a new Handler
        final Handler handler
                = new Handler(Looper.getMainLooper());

        // Call the post() method,
        // passing in a new Runnable.
        // The post() method processes
        // code without a delay,
        // so the code in the Runnable
        // will run almost immediately.
        handler.postDelayed(new Runnable() {
            @Override

            public void run()
            {
                refreshTimer();

                // If running is true, increment the
                // seconds variable.
                if (running) {
                    seconds++;
                }

                // Post the code again
                // with a delay of 1 second.
                handler.postDelayed(this, 1000);
            }
        }, 1000);
    }

    private void refreshTimer() {
        if (binding != null) {
            int hours = seconds / 3600;
            int minutes = (seconds % 3600) / 60;
            int secs = seconds % 60;

            // Format the seconds into hours, minutes,
            // and seconds.
            String time
                    = String
                    .format(Locale.getDefault(),
                            "%d:%02d:%02d", hours,
                            minutes, secs);

            binding.timeView.setText(time);
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}