package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

public class CreateProfile1 extends AppCompatActivity {

    Spinner accountTypeDropDown;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile1);

        // fetching xml elements
        accountTypeDropDown = findViewById(R.id.account_type_dropdown);

        // setting dropdown elements
        String[] accountTypeDropDownElements = new String[]{"Select Account-Type","Student (BPIT)","Faculty (BPIT)"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,accountTypeDropDownElements){
            @Override
            public boolean isEnabled(int position) {
                if (position == 0)
                    return false;
                else
                    return true;
            }
        };
        accountTypeDropDown.setAdapter(adapter);
    }
}
