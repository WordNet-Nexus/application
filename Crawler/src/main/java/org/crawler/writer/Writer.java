package org.crawler.writer;

import java.io.IOException;

public interface Writer {
    public void write(String fileName, String content) throws IOException;
}
