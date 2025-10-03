package com.example.sleep_application.ui.sleep_tracking_timer;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class SleepTrackingViewModel extends ViewModel {

    private final MutableLiveData<String> timerText;

    public SleepTrackingViewModel() {
        timerText = new MutableLiveData<>();
        timerText.setValue("0:00:00");
    }

    public LiveData<String> getText() {
        return timerText;
    }
}