package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.method.LinkMovementMethod;
import android.text.style.ClickableSpan;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    TextView termsAndConditionLink;
    Button agreeAndContinueBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // getting components from view
        termsAndConditionLink = findViewById(R.id.tc_link);
        agreeAndContinueBtn = findViewById(R.id.agree_btn);

        // creating termsAndConditionLink clickable
        SpannableString termsAndCondition = new SpannableString("Tap \"Agree and Continue\" to accept the Terms of Service and Privacy Policy.\nAlready Signup? Login");
        ClickableSpan termsAndConditionActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                startActivity(new Intent(MainActivity.this,TermsAndConditionActivity.class));
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setUnderlineText(false);
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setFakeBoldText(true);
            }
        };
        ClickableSpan privacyPolicyActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // start new activity
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
            }
        };
        ClickableSpan loginActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // launch login activity
                startActivity(new Intent(MainActivity.this,StudentLogin.class));
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
            }
        };
        termsAndCondition.setSpan(termsAndConditionActivityLauncher,39,55, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        termsAndCondition.setSpan(privacyPolicyActivityLauncher,60,74, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        termsAndCondition.setSpan(loginActivityLauncher,92,97,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        termsAndConditionLink.setText(termsAndCondition);
        termsAndConditionLink.setMovementMethod(LinkMovementMethod.getInstance());

        // setting event listener on agree_btn
        agreeAndContinueBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                startActivity(new Intent(MainActivity.this,CreateProfile1.class));
                startActivity(new Intent( MainActivity.this,FacultyLogin.class));
            }
        });
    }
}
