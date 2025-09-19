from uuid import UUID
from neurohub.base import BaseClient


class Transcriptions:
    def __init__(self, base: BaseClient):
        self._base = base

    def get_raw_transcription(self, file_uuid: UUID | str, client_uuid: UUID | str | None = None) -> str:
        """Fetch the raw content of the transcription file from S3.

        Args:
            file_uuid: The UUID of the file whose transcription is to be fetched.
            client_uuid: Optional client UUID for the request.

        Returns:
            The raw content of the TSV file as a string.

        Raises:
            RuntimeError: If the S3 client is not configured.
        """
        if not self._base.s3_bucket:
            raise RuntimeError("S3 client is not configured. Please provide AWS credentials when initializing the client.")
        client_uuid = self._base._handle_client_uuid(client_uuid)

        s3_key = f"transcript/{file_uuid}.tsv"
        response = self._base.s3_client.get_object(
            Bucket=self._base.s3_bucket,
            Key=s3_key
        )
        return response['Body'].read().decode('utf-8')
