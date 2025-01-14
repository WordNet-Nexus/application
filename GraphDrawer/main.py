from controller import Controller

if __name__ == "__main__":
    Controller.initialize(
        max_workers=2,         
        chunk_size=50000,
        upload_batch_size=1000
    )


