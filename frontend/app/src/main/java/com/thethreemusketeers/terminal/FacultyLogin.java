package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.style.ClickableSpan;
import android.view.View;
import android.widget.TextView;

public class FacultyLogin extends AppCompatActivity {

    TextView forgotPasswordLink , signUpLink;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_faculty_login);
        forgotPasswordLink = findViewById(R.id.forgot_password);
        signUpLink = findViewById(R.id.sign_up);

        SpannableString forgottenPassword = new SpannableString("Forgotten your details? Get help with signing in.");
        SpannableString signUp = new SpannableString("Don't have an account? Sign Up");
        ClickableSpan forgottenPasswordActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                //launch new activity
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds){
                ds.setUnderlineText(false);
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setFakeBoldText(true);
            }
        };

        ClickableSpan signUpActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                //launch new activity
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds){
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(true);
            }
        };



        forgottenPassword.setSpan(forgottenPasswordActivityLauncher, 24, 49, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        signUp.setSpan(signUpActivityLauncher, 23, 30,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        forgotPasswordLink.setText(forgottenPassword);
        signUpLink.setText(signUp);

    }
}
