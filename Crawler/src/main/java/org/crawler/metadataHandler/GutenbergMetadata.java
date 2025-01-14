package org.crawler.metadataHandler;

import org.json.JSONObject;

public class GutenbergMetadata implements GetMetadata{

    @Override
    public JSONObject getMetadata(String bookContent){
        String author = getAuthor(bookContent);
        String title = getTitle(bookContent);
        String date = getDate(bookContent);

        JSONObject json = new JSONObject();
        json.put("author", author);
        json.put("title", title);
        json.put("date", date);

        return json;
    }

    private String getAuthor(String bookContent){
        String regex = "Author: (.+?)(?=\\s*Release date:)";

        java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(regex);
        java.util.regex.Matcher matcher = pattern.matcher(bookContent);

        if (matcher.find()) {
            return matcher.group(1).trim();
        }

        return "Author not found";
    }

    private String getTitle(String bookContent){
        String regex = "Title: (.+?)(?=\\s*Author:)";

        java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(regex);
        java.util.regex.Matcher matcher = pattern.matcher(bookContent);

        if (matcher.find()) {
            return matcher.group(1).trim();
        }

        return "Title not found";

    }

    private String getDate(String bookContent){
        String regex = "Release date: (.+?)(?=\\s*\\[)";

        java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(regex);
        java.util.regex.Matcher matcher = pattern.matcher(bookContent);

        if (matcher.find()) {
            return matcher.group(1).trim();
        }

        return "Date not found";
    }

}
