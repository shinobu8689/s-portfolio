package com.example.sleep_application.ui.music_player;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.sleep_application.databinding.FragmentMusicBinding;

public class MusicFragment extends Fragment {

    private FragmentMusicBinding binding;
    private BackgroundMusicService backgroundMusicService;
    private boolean isBound = false;

    //setText needs a variable to work
    private String currentTrack = "Current Track: ";

    // manage connection between fragment to music service
    private ServiceConnection serviceConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            BackgroundMusicService.BackgroundMusicBinder binder = (BackgroundMusicService.BackgroundMusicBinder) service;
            backgroundMusicService = binder.getService();
            isBound = true;
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            backgroundMusicService = null;
            isBound = false;
        }
    };

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        MusicViewModel loginViewModel = new ViewModelProvider(this).get(MusicViewModel.class);

        binding = FragmentMusicBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        TextView textView = binding.textMusic;
        loginViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        // bind service to music service
        getActivity().bindService(new Intent(getActivity(), BackgroundMusicService.class), serviceConnection, Context.BIND_AUTO_CREATE);

        // initial button setup
        binding.stopBtn.setEnabled(false);
        binding.pauseBtn.setEnabled(false);
        binding.previousBtn.setEnabled(false);

        binding.newPlayButton.setOnClickListener(this::onClickPlay);
        binding.stopBtn.setOnClickListener(this::onClickStop);
        binding.pauseBtn.setOnClickListener(this::onClickPause);
        binding.previousBtn.setOnClickListener(this::onClickPrevious);
        binding.nextBtn.setOnClickListener(this::onClickNext);

        return root;
    }

    public void onClickPlay(View view) {
        if ( backgroundMusicService != null ) {
            backgroundMusicService.playSong();
            binding.textMusic.setText(currentTrack.concat(Integer.toString(backgroundMusicService.getCurrentSong())));
            updateButtons();
        }
    }

    public void onClickPause(View view) {
        if ( backgroundMusicService != null ) {
            backgroundMusicService.pauseSong();
            binding.textMusic.setText("Paused");
            updateButtons();
        }
    }

    public void onClickStop(View view) {
        if ( backgroundMusicService != null ) {
            backgroundMusicService.stopSong();
            binding.textMusic.setText("Stopped");
            updateButtons();
        }
    }

    public void onClickPrevious(View view) {
        if ( backgroundMusicService != null ) {
            backgroundMusicService.previousSong();
            binding.textMusic.setText(Integer.toString(backgroundMusicService.getCurrentSong()));
            updateButtons();
        }
    }

    public void onClickNext(View view) {
        if ( backgroundMusicService != null ) {
            backgroundMusicService.nextSong();
            binding.textMusic.setText(Integer.toString(backgroundMusicService.getCurrentSong()));
            updateButtons();
        }
    }


    private void updateButtons() {
        if ( backgroundMusicService != null ) {
            binding.newPlayButton.setEnabled(!backgroundMusicService.isPlaying());
            binding.pauseBtn.setEnabled(backgroundMusicService.isPlaying());
            binding.stopBtn.setEnabled(backgroundMusicService.isPlaying());
            binding.previousBtn.setEnabled(!backgroundMusicService.isMinMusic());
            binding.nextBtn.setEnabled(!backgroundMusicService.isMaxMusic());
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        // do not kill service
        // if (isBound) { getActivity().unbindService(serviceConnection); }
    }
}