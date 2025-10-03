package com.example.sleep_application.ui.home.sleeprecyclerview;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.sleep_application.R;
import com.example.sleep_application.database.entity.SleepEntity;

import java.time.temporal.ChronoUnit;
import java.util.ArrayList;

public class SleepEntityAdapter extends RecyclerView.Adapter<SleepEntityAdapter.ViewHolder> {
    private final ArrayList<SleepEntity> sleepData;
    private final Context context;

    public SleepEntityAdapter(ArrayList<SleepEntity> sleepData, Context context) {
        this.sleepData = sleepData;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.sleep_view_recycler_row, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        SleepEntity sleep = sleepData.get(position);
        long totalSecs = sleep.getDuration();
        long hours = totalSecs / 3600;
        long minutes = ((totalSecs % 3600) / 60);
        long seconds = totalSecs % 60;

        Log.println(Log.DEBUG, "test", String.valueOf(sleep.getDuration()));

        holder.durationTv.setText(String.format("%02d:%02d:%02d", hours, minutes, seconds));
        holder.endTimeTv.setText(sleep.getFinishTime().truncatedTo(ChronoUnit.SECONDS).toString());
        holder.startTimeTv.setText(sleep.getFinishTime().minus(totalSecs, ChronoUnit.SECONDS).truncatedTo(ChronoUnit.SECONDS).toString());
        holder.dateTv.setText(sleep.getDate().toString());

    }

    @Override
    public int getItemCount() {
        return sleepData.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {


        private final TextView durationTv;
        private final TextView startTimeTv;
        private final TextView endTimeTv;
        private final TextView dateTv;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            durationTv = itemView.findViewById(R.id.durationContentTv);
            startTimeTv = itemView.findViewById(R.id.startTimeContentTv);
            endTimeTv = itemView.findViewById(R.id.endTimeContentTv);
            dateTv = itemView.findViewById(R.id.dateTv);
        }
    }
}
