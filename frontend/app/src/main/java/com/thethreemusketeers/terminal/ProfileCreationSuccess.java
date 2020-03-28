package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;
import androidx.vectordrawable.graphics.drawable.AnimatedVectorDrawableCompat;

import android.graphics.drawable.AnimatedVectorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.widget.ImageView;

public class ProfileCreationSuccess extends AppCompatActivity {

    ImageView checkMark;
    AnimatedVectorDrawable avd;
    AnimatedVectorDrawableCompat avdc;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile_creation_success);

        // FETCHING COMPONENTS FROM XML PAGE
        checkMark = findViewById(R.id.check_mark);

        // STARTING CHECK MARK ANIMATION
        Drawable drawable = checkMark.getDrawable();
        if ( drawable instanceof AnimatedVectorDrawableCompat ) {
            avdc = (AnimatedVectorDrawableCompat) drawable;
            avdc.start();
        }
        else if ( drawable instanceof  AnimatedVectorDrawable) {
            avd = (AnimatedVectorDrawable) drawable;
            avd.start();
        }

        // LOGGING USER INTO THE DASHBOARD ACTIVITY

    }
}
