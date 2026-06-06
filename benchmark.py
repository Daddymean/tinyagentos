import asyncio
import time
from tinyagentos.training import TrainingManager
import tempfile
from pathlib import Path

async def run_benchmark():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        mgr = TrainingManager(db_path)
        await mgr.init()

        # create a dummy job
        job_id = await mgr.create_job(base_model="test-model")

        # The fields we want to update
        kwargs = {
            "status": "training",
            "progress": 0.5,
            "worker_name": "worker-1",
            "metrics": {"loss": 0.1, "accuracy": 0.9},
            "output_path": "/tmp/output",
            "error": "none",
            "completed_at": 1234567890.0,
        }

        # Warm up
        for _ in range(10):
            await mgr.update_job(job_id, **kwargs)

        num_iterations = 1000
        start_time = time.time()

        for _ in range(num_iterations):
            await mgr.update_job(job_id, **kwargs)

        end_time = time.time()
        print(f"Time for {num_iterations} updates: {end_time - start_time:.4f} seconds")

        await mgr.close()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
