package org.crawler;

import org.crawler.controller.BookController;
import org.crawler.downloadHandlers.GutenbergDownloadHandler;
import org.crawler.metadataHandler.GutenbergMetadata;
import org.crawler.model.NumbersInRange;
import org.crawler.writer.AWSWriter;

import java.util.List;

public class Controller {

    public static void execute(String bucketname, Integer start, Integer end){
        BookController controller = new BookController(new GutenbergDownloadHandler(), new AWSWriter(bucketname),
                new GutenbergMetadata());

        List<Integer> bookIDs = NumbersInRange.createBooksIDs(start, end);
        controller.downloadBooks(bookIDs);

    }
}
