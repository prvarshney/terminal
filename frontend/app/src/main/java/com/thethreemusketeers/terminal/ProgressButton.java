package com.thethreemusketeers.terminal;

import android.app.Activity;
import android.content.Context;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.cardview.widget.CardView;
import androidx.constraintlayout.widget.ConstraintLayout;

public class ProgressButton {

    private CardView cardView;
    private ConstraintLayout constraintLayout;
    private ProgressBar progressBar;
    private TextView textView;

    public ProgressButton(Context context, View view) {
        cardView = view.findViewById(R.id.card_view);
        constraintLayout = view.findViewById(R.id.constraint_layout);
        progressBar = view.findViewById(R.id.progressBar);
        textView = view.findViewById(R.id.textView);
    }

    public void buttonProgressActivatedState( String msg ) {
        progressBar.setVisibility(View.VISIBLE);
        textView.setText(msg);
    }

    public void buttonProgressStoppedState( String msg ) {
        progressBar.setVisibility(View.INVISIBLE);
        textView.setText(msg);
    }

}
