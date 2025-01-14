package org.crawler.controller;

import org.crawler.downloadHandlers.DownloadHandler;
import org.crawler.metadataHandler.GetMetadata;
import org.crawler.model.Book;
import org.crawler.writer.Writer;
import org.json.JSONObject;
import org.jsoup.nodes.Document;

import java.io.IOException;
import java.util.List;

public class BookController {
    private final DownloadHandler downloadHandler;
    private final Writer writer;
    private final GetMetadata metadataHandler;

    public BookController(DownloadHandler downloadHandler, Writer writer, GetMetadata metadataHandler) {
        this.downloadHandler = downloadHandler;
        this.writer = writer;
        this.metadataHandler = metadataHandler;
    }

    public void downloadBooks(List<Integer> bookIDs) {

        for (int bookID : bookIDs) {
            try {
                Document bookDocument = downloadHandler.handleDownload(bookID);
                if (bookDocument != null) {
                    String content = bookDocument.text();

                    JSONObject metadata = metadataHandler.getMetadata(content);
                    Book book = new Book(metadata.getString("title"),
                            metadata.getString("author"),metadata.getString("date"),
                            bookID,  content);

                    writer.write(bookID + ".txt", content);

                    System.out.println("Download: " + book.id());
                }
                else{
                    continue;
                }
            }
                 catch (IOException e) {
                System.err.println("Error downloading book with ID " + bookID + ": " + e.getMessage());
            }
        }
    }


}
