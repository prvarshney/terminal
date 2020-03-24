package com.thethreemusketeers.terminal;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.DialogFragment;

import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;

import java.util.Calendar;

public class DatePickerFragment extends DialogFragment {
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        int month;
        int day;
        int year;
        Calendar calendar = Calendar.getInstance();
        // CHECKING WHETHER USER HAS SELECTED ANY DATE PREVIOUSLY
        if ( UserRegisterObject.dob.equals("") )    // IF USER DOESN'T SELECTED ANY DATE PRESENTING
        {                                           // HIM/HER TODAY'S DATE
            year = calendar.get(Calendar.YEAR);
            month = calendar.get(Calendar.MONTH);
            day = calendar.get(Calendar.DAY_OF_MONTH);
        }
        else {                  // PRESENTING PREVIOUSLY SELECTED DATE TO USER
            String date = UserRegisterObject.dob;
            String[] dateArr = date.split("/");
            day = Integer.valueOf(dateArr[0]);      // CAN BE USE AS IT IS
            month = Integer.valueOf(dateArr[1]) - 1;    // BECAUSE MONTH STARTS FROM 0-11
            year = Integer.valueOf(dateArr[2]);     // CAN BE USE AS IT IS
        }
        DatePickerDialog dialog = new DatePickerDialog(getActivity(), (DatePickerDialog.OnDateSetListener) getActivity(), year, month, day);
        dialog.getDatePicker().setMaxDate(calendar.getTimeInMillis());
        return dialog;
    }
}