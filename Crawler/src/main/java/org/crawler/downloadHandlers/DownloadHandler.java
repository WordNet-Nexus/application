package org.crawler.downloadHandlers;

import org.jsoup.nodes.Document;

import java.io.IOException;

public interface DownloadHandler {
    abstract Document handleDownload(int bookID) throws IOException;
}
