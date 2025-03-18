using System.Diagnostics;

public class StopwatchContext : Stopwatch, IDisposable
{
    public StopwatchContext()
    {
        Start();
    }

    public void Dispose()
    {
        Stop();
    }
}
