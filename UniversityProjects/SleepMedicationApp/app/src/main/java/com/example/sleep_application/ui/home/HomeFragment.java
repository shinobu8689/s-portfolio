package com.example.sleep_application.ui.home;

import static java.lang.String.format;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.res.Resources;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.ColorInt;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.room.Room;

import com.example.sleep_application.database.LocalSqlDbService;
import com.example.sleep_application.database.entity.SleepEntity;
import com.example.sleep_application.databinding.FragmentHomeBinding;
import com.example.sleep_application.ui.home.sleeprecyclerview.SleepEntityAdapter;
import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.ValueFormatter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;

    public static int getThemeTextColor(Context context) {
        TypedValue typedValue = new TypedValue();
        Resources.Theme theme = context.getTheme();
        theme.resolveAttribute(com.google.android.material.R.attr.colorOnSecondary, typedValue, true);
        @ColorInt int color = typedValue.data;
        return color;
    }


    private static class BarchartFormatter extends ValueFormatter {
        BarDataSet barDataSet;

        public BarchartFormatter(BarDataSet barDataSet) {
            this.barDataSet = barDataSet;
        }

        @Override
        public String getBarLabel(BarEntry barEntry) {
            return format("%.2f Hours", barEntry.getY());

        }

        @Override
        public String getAxisLabel(float value, AxisBase axis) {
            return ((LocalDate) barDataSet.getValues().get((int) value)
                    .getData())
                    .format(DateTimeFormatter.ofPattern("MM/dd"));
        }
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
//        HomeViewModel homeViewModel =
//                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        RecyclerView recyclerView = binding.sleepLogRecycler;

        LocalSqlDbService dbService = Room.databaseBuilder(requireActivity().getApplicationContext(), LocalSqlDbService.class, "appDb")
                .allowMainThreadQueries().build();


        SharedPreferences sharedPref = getActivity().getPreferences(Context.MODE_PRIVATE);
        String email = sharedPref.getString("login_email", "No email");

        ArrayList<SleepEntity> sleepData = new ArrayList<>(dbService.sleepDao().getAllByUser(email));

        sleepData.sort(Comparator.comparing(SleepEntity::getDate).thenComparing(SleepEntity::getFinishTime).reversed());


        SleepEntityAdapter sleepEntityAdapter = new SleepEntityAdapter(sleepData, this.getContext());
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this.getContext(), LinearLayoutManager.VERTICAL, false);

        recyclerView.setLayoutManager(linearLayoutManager);
        recyclerView.setAdapter(sleepEntityAdapter);

        sleepEntityAdapter.notifyDataSetChanged();

        BarChart barChart = binding.chart1;

        List<BarEntry> barEntryList = new ArrayList<>();
        List<SleepEntity> reverseSleepList = (List<SleepEntity>) sleepData.clone();
        Collections.reverse(reverseSleepList);

        int count = 0;
        LocalDate date = null;
        for (SleepEntity sleepEntity : reverseSleepList) {
            if (date != null && sleepEntity.getDate().isEqual(date)) {
                BarEntry barEntry = barEntryList.get(barEntryList.size() - 1);
                barEntry.setY(barEntry.getY() + ((float) sleepEntity.getDuration()) / 60 / 60);
            } else {
                date = sleepEntity.getDate();
                barEntryList.add(new BarEntry(count, ((float) sleepEntity.getDuration()) / 60 / 60, date));
                count++;
            }
        }

        BarDataSet set = new BarDataSet(barEntryList, "SleepDataSet");

        BarData data = new BarData(set);
        data.setBarWidth(0.8f); // set custom bar width
        data.setValueFormatter(new BarchartFormatter(set));
        barChart.setData(data);
        barChart.setFitBars(true); // make the x-axis fit exactly all bars

        int color = getThemeTextColor(requireContext());
        barChart.getData().setValueTextColor(color);
        barChart.getData().setValueTextColor(color);
        barChart.getXAxis().setTextColor(color);
        barChart.getAxisLeft().setTextColor(color);
        barChart.getAxisRight().setTextColor(color);
        barChart.getLegend().setTextColor(color);

        barChart.setDrawValueAboveBar(false);
        barChart.setDrawGridBackground(false);
        Description emptyDescription = new Description();
        emptyDescription.setText("");
        barChart.setDescription(emptyDescription);

        barChart.getAxisLeft().setAxisMinimum(0);
        barChart.getAxisLeft().setDrawGridLines(false);

        XAxis xAxis = barChart.getXAxis();
        xAxis.setDrawGridLines(false);
        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
        xAxis.setTextSize(10f);
        xAxis.setLabelRotationAngle(0);
        xAxis.setValueFormatter(new BarchartFormatter(set));
        barChart.invalidate(); // refresh
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}