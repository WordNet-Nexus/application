package org.crawler.writer;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.ObjectMetadata;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

public class AWSWriter implements Writer{

    private final AmazonS3 s3Client;
    private final String bucketName;

    public AWSWriter(String bucketName){
        this.bucketName = bucketName;
        this.s3Client = AmazonS3ClientBuilder.standard().build();
        createBucket();
    }
    @Override
    public void write(String fileName, String content) throws IOException {
        try {
            InputStream inputStream = new ByteArrayInputStream(content.getBytes());
            ObjectMetadata metadata = new ObjectMetadata();
            metadata.setContentLength(content.length());

            s3Client.putObject(bucketName, fileName, inputStream, metadata);
        } catch (Exception e) {
            throw new IOException("Error uploading the book to the S3: " + e.getMessage(), e);
        }
    }
    private void createBucket() {
        try {
            s3Client.createBucket(bucketName);
        } catch (Exception e) {
            System.err.println("Error creating the bucket: " + e.getMessage());
        }
    }
}
