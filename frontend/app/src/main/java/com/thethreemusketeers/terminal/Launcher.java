package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

import com.thethreemusketeers.terminal.Activities.MainActivity;

public class Launcher extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launcher);
        startActivity(new Intent(Launcher.this, MainActivity.class));
    }
}
