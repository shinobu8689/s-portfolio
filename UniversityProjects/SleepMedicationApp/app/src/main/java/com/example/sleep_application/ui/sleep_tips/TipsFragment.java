package com.example.sleep_application.ui.sleep_tips;

import static java.lang.Math.round;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.room.Room;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.sleep_application.database.LocalSqlDbService;
import com.example.sleep_application.database.entity.SleepEntity;
import com.example.sleep_application.databinding.FragmentTipsBinding;
import com.google.android.material.snackbar.Snackbar;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;

public class TipsFragment extends Fragment {

    private FragmentTipsBinding binding;

    private TipsViewModel mViewModel;

    LocalSqlDbService dbService;

    ArrayList<SleepEntity> sleepData = null;

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {


        binding = FragmentTipsBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        dbService = Room.databaseBuilder(requireActivity().getApplicationContext(), LocalSqlDbService.class, "appDb")
                .allowMainThreadQueries().build();


        SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
        String email = sharedPref.getString("login_email", "No email");
        sleepData = new ArrayList<>(dbService.sleepDao().getAllByUser(email));

        binding.textView2.setText(analysis());

        binding.undersleepBtn.setOnClickListener(this::onClickDebugUnderSleep);
        binding.goodsleepBtn.setOnClickListener(this::onClickDebugAvgSleep);
        binding.oversleepBtn.setOnClickListener(this::onClickDebugOverSleep);

        return root;
    }

    public String analysis(){
        int sleep_size = sleepData.size();
        long seven = sleepData.stream().filter(entity -> 25200 > entity.getDuration()).count();
        long nine = sleepData.stream().filter(entity -> 32400 < entity.getDuration()).count();
        long normal = sleep_size - seven - nine;
        long total_sleep_duration = 0;
        for (SleepEntity entity : sleepData) { total_sleep_duration += entity.getDuration(); }
        double avg = (double) total_sleep_duration / (double) sleep_size / 3600;

        double goodsleep_hrs_p  = (double) normal / (double) sleep_size;
        double undersleep_hrs_p = (double) seven / (double) sleep_size;
        double oversleep_hrs_p  = (double) nine / (double) sleep_size;

        String analysis = "";

        if (sleep_size <= 0) {  // if sleep_size <= 0, not enough record
            analysis += "You have no sleep record.\nGo get some sleep.";
        } else {
            analysis += "In total of " + sleep_size + " sleep record:\n";
            analysis += "You have average of " + (double) (((int) (avg * 100)))/100 + " hrs of sleep.\n";
            analysis += (int) (goodsleep_hrs_p * 100) + "% of your sleeps have desirable length.\n";
            analysis += (int) (undersleep_hrs_p * 100) + "% of your sleeps are less than 7 hours.\n";
            analysis += (int) (oversleep_hrs_p * 100) + "% of your sleeps are more than 9 hours.\n";
            if ((undersleep_hrs_p > 0.4) && (oversleep_hrs_p > 0.4)) {
                analysis += "Your sleep is irregular.\nConsider fixed sleep pattern.";
            } else if (undersleep_hrs_p > 0.4) {
                analysis += "You need more sleep, try some relaxation methods.";
            } else if (oversleep_hrs_p > 0.4) {
                analysis += "You are sleeping too much, try setting alarm to wakeup.";
            } else {
                analysis += "You having good sleep, keep it up!";
            }
        }
        return analysis;
    }

    public void onClickDebugUnderSleep(View view) { addSleepRecord(view, 24000); }

    public void onClickDebugAvgSleep(View view) { addSleepRecord(view, 30000); }

    public void onClickDebugOverSleep(View view) { addSleepRecord(view, 32760); }

    private void addSleepRecord(View view, int sec) {
        SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
        String email = sharedPref.getString("login_email", "No email");
        SleepEntity sleepEntity = new SleepEntity(email, LocalDate.now(), LocalTime.now(), sec);
        dbService.sleepDao().insertAll(sleepEntity);
        Snackbar.make(view, new StringBuffer("Added record."), Snackbar.LENGTH_SHORT).show();
    }

}