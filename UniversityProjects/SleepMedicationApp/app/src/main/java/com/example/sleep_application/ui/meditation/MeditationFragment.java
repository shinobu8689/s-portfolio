package com.example.sleep_application.ui.meditation;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.sleep_application.R;
import com.example.sleep_application.databinding.FragmentMeditationBinding;
import com.google.android.material.snackbar.Snackbar;

import java.util.Locale;

public class MeditationFragment extends Fragment {

    private @NonNull FragmentMeditationBinding binding;

    // img set for different sessions types
    private static final int[] BREATH_IMG = {R.drawable.breath1, R.drawable.breath2, R.drawable.breath3};
    private static final int[] STRETCH_IMG = {R.drawable.stretch1, R.drawable.stretch2, R.drawable.stretch3, R.drawable.stretch4};
    private static final int[] AEROBIC_IMG = {R.drawable.aerobic1, R.drawable.aerobic2, R.drawable.aerobic3, R.drawable.aerobic4};
    private static final int SLIDE_DURATION = 3000; // milliseconds

    private int med_seconds = 60;
    private int inputted_mins = 60;
    private boolean med_running;

    AlertDialog.Builder builder;
    private MediaPlayer mediaPlayer;


    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        MeditationViewModel meditationViewModel =
                new ViewModelProvider(this).get(MeditationViewModel.class);

        binding = FragmentMeditationBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textMedTimer;
        meditationViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        // set default session length for 5 mins
        binding.inputMins.setText("5");

        // init popup builder
        builder = new AlertDialog.Builder(getActivity());

        // setup dropdown menu
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(getActivity(), R.array.array_meditation, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        binding.meditationSpinner.setAdapter((adapter));

        // guide slideshow img
        binding.meditationSlideshow.setInAnimation(AnimationUtils.loadAnimation(getActivity(), R.anim.slide_in_right));
        binding.meditationSlideshow.setOutAnimation(AnimationUtils.loadAnimation(getActivity(), R.anim.slide_out_left));
        binding.meditationSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                switchImgSet(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // Handle no selection case (optional)
            }
        });
        binding.medStartBtn.setOnClickListener(this::onClickStart);
        startSlideShow(); // scroll through meditation guide img

        refreshMedTimer();

        // music setup
        mediaPlayer = MediaPlayer.create(getActivity(), R.raw.m06);
        mediaPlayer.setLooping(true);

        binding.medStartBtn.setOnClickListener(this::onClickStart);
        binding.medPauseBtn.setOnClickListener(this::onClickPause);
        binding.medResetBtn.setOnClickListener(this::onClickSet);

        runMedTimer();

        return root;
    }

    private void startSlideShow() { // setup image set
        final Handler med_handler = new Handler();
        med_handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (binding != null) { binding.meditationSlideshow.showNext(); }
                med_handler.postDelayed(this, SLIDE_DURATION);
            }
        }, SLIDE_DURATION);
    }

    private void onClickStart(View view) { // start countdown and play music
        mediaPlayer = MediaPlayer.create(getActivity(), R.raw.m06);
        mediaPlayer.setLooping(true);
        if (med_seconds <= 0) {
            Snackbar.make(view, new StringBuffer("You need to set the timer."), Snackbar.LENGTH_SHORT).show();
        } else {
            med_running = true;
            if ( !mediaPlayer.isPlaying() ) { mediaPlayer.start(); }
        }
    }

    private void onClickPause(View view) { // pause counter and music
        med_running = false;
        if ( mediaPlayer.isPlaying() ) { mediaPlayer.pause(); }
    }

    private void onClickSet(View view) { // apply inputted valid value to the timer
        med_running = false;
        mediaPlayer.stop();
        String inputMins = binding.inputMins.getText().toString();
        if (inputMins.matches("")) {
            Snackbar.make(view, new StringBuffer("Minutes could not be empty."), Snackbar.LENGTH_SHORT).show();
        } else {
            inputted_mins = 60 * Integer.parseInt(inputMins);
            med_seconds = inputted_mins;
        }
    }

    private void runMedTimer() {
        final Handler handler = new Handler(Looper.getMainLooper());
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                refreshMedTimer();
                if (med_running) { med_seconds--; }
                if (med_seconds < 0) {  // session ended

                    // stop counter and music
                    med_running = false;
                    med_seconds = inputted_mins;
                    mediaPlayer.stop();

                    // create finish dialog
                    builder.setMessage("Enjoy your sleep.")
                            .setTitle("You have finished your session")
                            .setCancelable(false)
                            .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int id) { }
                            });
                    AlertDialog alert = builder.create();
                    alert.show();

                }
                handler.postDelayed(this, 1000);
            }
        }, 1000);
    }


    //switch img set according to each session type
    private void switchImgSet(Integer position){
        binding.meditationSlideshow.removeAllViews();
        int[] IMG_SET = {};

        switch (position) {
            case 0:
                IMG_SET = BREATH_IMG;
                break;
            case 1:
                IMG_SET = STRETCH_IMG;
                break;
            case 2:
                IMG_SET = AEROBIC_IMG;
                break;
        }

        for (int imageId : IMG_SET) {
            ImageView imageView = new ImageView(getActivity());
            imageView.setImageResource(imageId);
            binding.meditationSlideshow.addView(imageView);
        }
    }

    private void refreshMedTimer() {
        if (binding != null) {
            int minutes = (med_seconds % 3600) / 60;
            int secs = med_seconds % 60;
            String time = String.format(Locale.getDefault(),"%02d:%02d", minutes, secs);
            binding.textMedTimer.setText(time);
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
        if (mediaPlayer != null) {
            mediaPlayer.release();
        }
    }


}