import { useEffect, useState } from "react";
import { API } from "./api";

function App() {
  const [segments, setSegments] = useState([]);
  const [selected, setSelected] = useState(null);
  const [added, setAdded] = useState([]);
  const [removed, setRemoved] = useState([]);

  useEffect(() => {
    API.get("/segments/")
      .then((res) => setSegments(res.data))
      .catch(() => setSegments([]));
  }, []);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/segments/");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (selected && data.segment_id === selected.id) {
        setAdded(data.added);
        setRemoved(data.removed);
      }
    };

    return () => ws.close();
  }, [selected]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Segments</h1>

      <ul>
        {segments.map((seg) => (
          <li key={seg.id}>
            <button onClick={() => setSelected(seg)}>{seg.name}</button>
          </li>
        ))}
      </ul>

      {selected && (
        <div style={{ marginTop: 20 }}>
          <h2>{selected.name}</h2>

          <h3>🟢 Added</h3>
          <ul>
            {added.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>

          <h3>🔴 Removed</h3>
          <ul>
            {removed.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
