package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;

import com.thethreemusketeers.terminal.R;

public class Launcher extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launcher);

        // CHECKING WHETHER USER IS ALREADY LOGGEDIN OR NOT
        SharedPreferences sharedPref = this.getSharedPreferences(getString(R.string.user_credentials_file_key),Context.MODE_PRIVATE);
        boolean isLoggedIn = sharedPref.getBoolean(getString(R.string.login_status),false);
        // IF USER IS NOT LOGGED IN ROUTING HIM/HER TO MAIN_ACTIVITTY AFTER 2000MS
        if ( !isLoggedIn ) {
            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    startActivity(new Intent(Launcher.this, MainActivity.class));
                }
            },1500);
        }
        else {
            // CONNECTING WITH SERVER TO FETCH DASHBOARD
            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    startActivity(new Intent(Launcher.this, Dashboard.class));
                }
            },2000);
        }
    }
}
