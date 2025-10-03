package com.example.sleep_application.ui.meditation;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class MeditationViewModel extends ViewModel {
    private final MutableLiveData<String> timerText;

    public MeditationViewModel() {
        timerText = new MutableLiveData<>();
        timerText.setValue("TIMER");
    }

    public LiveData<String> getText() {
        return timerText;
    }
}