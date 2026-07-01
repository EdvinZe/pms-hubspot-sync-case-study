from src.sync.guesty_sync import run_guesty_sync
from src.sync.hostaway_sync import run_hostaway_sync
from src.sync.logger import log_event


def main() -> dict:
    log_event("sync_runner_started")
    guesty_result = run_guesty_sync()
    hostaway_result = run_hostaway_sync()
    log_event("sync_runner_finished")
    return {"guesty": guesty_result, "hostaway": hostaway_result}


if __name__ == "__main__":
    main()
