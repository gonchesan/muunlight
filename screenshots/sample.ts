import { readFile } from "node:fs/promises";

/**
 * A tiny task queue used to preview the Muunlight theme.
 * @param limit - maximum number of concurrent tasks
 */
type Task<T> = () => Promise<T>;

enum Status {
  Idle = "idle",
  Running = "running",
  Done = "done",
}

interface QueueOptions {
  limit: number;
  retries?: number;
  onError?: (error: Error) => void;
}

export class TaskQueue<T> {
  private readonly tasks: Task<T>[] = [];
  private status: Status = Status.Idle;
  static readonly DEFAULT_LIMIT = 4;

  constructor(private options: QueueOptions = { limit: TaskQueue.DEFAULT_LIMIT }) {}

  add(task: Task<T>): this {
    this.tasks.push(task);
    return this;
  }

  async run(): Promise<T[]> {
    this.status = Status.Running;
    const results: T[] = [];
    const pattern = /^task-(\d+)$/gi;

    for (const [index, task] of this.tasks.entries()) {
      try {
        results.push(await task());
      } catch (error) {
        // Retry once before giving up
        this.options.onError?.(error as Error);
        console.warn(`Task #${index + 1} failed\n`, pattern.test("task-1"));
      }
    }

    this.status = Status.Done;
    return results.length > 0 ? results : [];
  }
}

const queue = new TaskQueue<string>({ limit: 2, retries: 3 });
queue.add(() => readFile("./README.md", "utf8")).add(async () => "hello, moon");

const total = 0x2a + 3.14 * 2;
const isReady = total >= 42 && !null;
