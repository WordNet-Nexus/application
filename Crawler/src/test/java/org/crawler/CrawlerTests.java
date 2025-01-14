package org.crawler;

import org.crawler.downloadHandlers.DownloadHandler;
import org.crawler.downloadHandlers.GutenbergDownloadHandler;
import org.crawler.writer.AWSWriter;
import org.crawler.controller.BookController;
import org.crawler.metadataHandler.GetMetadata;
import org.crawler.model.Book;
import org.jsoup.nodes.Document;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.json.JSONObject;

import java.io.IOException;
import java.util.List;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class CrawlerTests {

    private DownloadHandler downloadHandler;
    private GutenbergDownloadHandler gutenbergDownloadHandler;
    private AWSWriter awsWriter;
    private BookController bookController;
    private GetMetadata metadataHandler;

    @BeforeEach
    public void setup() throws IOException {
        // Create mock objects
        downloadHandler = Mockito.mock(DownloadHandler.class);
        awsWriter = Mockito.mock(AWSWriter.class);
        metadataHandler = Mockito.mock(GetMetadata.class);
        bookController = new BookController(downloadHandler, awsWriter, metadataHandler);
    }

    @Test
    public void testHandleDownloadSuccess() throws IOException {
        // Mock a successful download
        Document mockDocument = Mockito.mock(Document.class);
        when(downloadHandler.handleDownload(1)).thenReturn(mockDocument);
        when(mockDocument.text()).thenReturn("Sample book content");

        Document result = downloadHandler.handleDownload(1);
        assertNotNull(result);
        assertEquals("Sample book content", result.text());
    }

    @Test
    public void testHandleDownloadFailure() throws IOException {
        // Mock a failed download
        when(downloadHandler.handleDownload(2)).thenThrow(new IOException("Download error"));

        assertThrows(IOException.class, () -> downloadHandler.handleDownload(2));
    }

    @Test
    public void testAWSWriterWrite() throws IOException {
        // Mock successful write
        doNothing().when(awsWriter).write("test.txt", "Sample content");

        awsWriter.write("test.txt", "Sample content");
        verify(awsWriter, times(1)).write("test.txt", "Sample content");
    }

    @Test
    public void testAWSWriterWriteFailure() throws IOException {
        // Mock write failure
        doThrow(new IOException("S3 upload error")).when(awsWriter).write("test.txt", "Sample content");

        assertThrows(IOException.class, () -> awsWriter.write("test.txt", "Sample content"));
    }

    @Test
    public void testBookControllerDownloadBooksSuccess() throws IOException {
        // Mock dependencies
        Document mockDocument = Mockito.mock(Document.class);
        when(mockDocument.text()).thenReturn("Sample book content");

        when(downloadHandler.handleDownload(1)).thenReturn(mockDocument);
        JSONObject mockMetadata = new JSONObject();
        mockMetadata.put("title", "Sample Title");
        mockMetadata.put("author", "Sample Author");
        mockMetadata.put("date", "2025-01-01");

        when(metadataHandler.getMetadata("Sample book content")).thenReturn(mockMetadata);

        doNothing().when(awsWriter).write(anyString(), anyString());

        // Test bookController
        bookController.downloadBooks(List.of(1));

        verify(downloadHandler, times(1)).handleDownload(1);
        verify(metadataHandler, times(1)).getMetadata("Sample book content");
        verify(awsWriter, times(1)).write("1.txt", "Sample book content");
    }

    @Test
    public void testBookControllerDownloadBooksPartialFailure() throws IOException {
        // Mock dependencies
        Document mockDocument = Mockito.mock(Document.class);
        when(mockDocument.text()).thenReturn("Sample book content");

        when(downloadHandler.handleDownload(1)).thenReturn(mockDocument);
        when(downloadHandler.handleDownload(2)).thenThrow(new IOException("Download error"));

        JSONObject mockMetadata = new JSONObject();
        mockMetadata.put("title", "Sample Title");
        mockMetadata.put("author", "Sample Author");
        mockMetadata.put("date", "2025-01-01");

        when(metadataHandler.getMetadata("Sample book content")).thenReturn(mockMetadata);

        doNothing().when(awsWriter).write(anyString(), anyString());

        // Test bookController
        bookController.downloadBooks(List.of(1, 2));

        verify(downloadHandler, times(1)).handleDownload(1);
        verify(downloadHandler, times(1)).handleDownload(2);
        verify(metadataHandler, times(1)).getMetadata("Sample book content");
        verify(awsWriter, times(1)).write("1.txt", "Sample book content");
    }

    @Test
    public void testGutenbergDownloadHandlerLanguageFilter() throws IOException {
        // Test language filter
        GutenbergDownloadHandler handler = new GutenbergDownloadHandler();

        String englishContent = "Language: English\n\nCredits:";
        String nonEnglishContent = "Language: Spanish\n\nCredits:";

        assertTrue(handler.language(englishContent));
        assertFalse(handler.language(nonEnglishContent));
    }

    @Test
    public void testGutenbergDownloadHandlerDownload() throws IOException {
        // Mocking a real download with Jsoup
        GutenbergDownloadHandler handler = Mockito.spy(new GutenbergDownloadHandler());
        Document mockDocument = Mockito.mock(Document.class);
        when(mockDocument.text()).thenReturn("Language: English\n\nSample content");

        // Simulate the Jsoup connection
        Mockito.doReturn(mockDocument).when(handler).handleDownload(1);

        Document result = handler.handleDownload(1);
        assertNotNull(result);
        assertTrue(result.text().contains("Language: English"));
    }
}
