import { useEffect, useState, useRef } from "react";
import API from "./api";

function App() {
  const [segments, setSegments] = useState([]);
  const [selected, setSelected] = useState(null);
  const [added, setAdded] = useState([]);
  const [removed, setRemoved] = useState([]);

  const wsRef = useRef(null);
  const selectedRef = useRef(null);

  useEffect(() => {
    selectedRef.current = selected;
  }, [selected]);

  useEffect(() => {
    API.get("/segments/")
      .then((res) => setSegments(res.data))
      .catch(() => setSegments([]));
  }, []);

  useEffect(() => {
    if (segments.length > 0 && !selected) {
      setSelected(segments[0]);
    }
  }, [segments]);

  useEffect(() => {
    if (wsRef.current) return;

    const ws = new WebSocket("ws://127.0.0.1:8000/ws/segments/");
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      const currentSelected = selectedRef.current;

      if (!currentSelected || data.segment_id === currentSelected.id) {
        setAdded(data.added || []);
        setRemoved(data.removed || []);
      }
    };
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Segments</h1>

      <ul>
        {segments.map((seg) => (
          <li key={seg.id}>
            <button
              onClick={() => {
                setSelected(seg);
                setAdded([]);
                setRemoved([]);
              }}
              style={{
                fontWeight: selected?.id === seg.id ? "bold" : "normal",
              }}
            >
              {seg.name}
            </button>
          </li>
        ))}
      </ul>

      <div style={{ marginTop: 20 }}>
        <h2>{selected ? selected.name : "No segment selected"}</h2>

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
    </div>
  );
}

export default App;
