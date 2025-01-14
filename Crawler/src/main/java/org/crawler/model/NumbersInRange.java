package org.crawler.model;

import java.util.ArrayList;
import java.util.List;

public class NumbersInRange {

    public static List<Integer> createBooksIDs(int min, int max) {
        List<Integer> booksIDs = new ArrayList<>();
        for (int i = min; i <= max; i++) {
            booksIDs.add(i);
        }
        return booksIDs;
    }
}
