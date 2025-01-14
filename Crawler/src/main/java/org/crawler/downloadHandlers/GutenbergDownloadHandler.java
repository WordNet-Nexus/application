package org.crawler.downloadHandlers;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.IOException;

public class GutenbergDownloadHandler implements DownloadHandler {
    private static final String PROJECT_GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt";

    @Override
    public Document handleDownload(int bookID) throws IOException {
        String bookUrl = PROJECT_GUTENBERG_URL.replace("{id}", String.valueOf(bookID));
        Document bookDocument = Jsoup.connect(bookUrl).get();
        if (language(bookDocument.text()) == true){
            return bookDocument;
        }
        else{
            return null;
        }
    }

    public boolean language(String bookContent){
        String regex = "Language: (.+?)(?=\\s*Credits:)";

        java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(regex);
        java.util.regex.Matcher matcher = pattern.matcher(bookContent);

        if (matcher.find()) {
            String language = matcher.group(1).trim();
            return language.equalsIgnoreCase("English");
        }

        return false;
    }
}
