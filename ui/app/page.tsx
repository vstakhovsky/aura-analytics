"use client";
import { useState } from "react";
import { marked } from "marked";

const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Home() {
  const [md, setMd] = useState<string>("");
  const [insights, setInsights] = useState<any[]>([]);
  const [busy, setBusy] = useState<boolean>(false);
  const [contract, setContract] = useState<any>(null);

  async function ingestSample() {
    setBusy(true);
    await fetch(`${API}/ingest/sample`, { method: "POST" });
    setBusy(false);
  }
  async function uploadFile(f: File) {
    const fd = new FormData(); fd.append("file", f);
    setBusy(true);
    await fetch(`${API}/ingest`, { method: "POST", body: fd });
    setBusy(false);
  }
  async function analyze() {
    setBusy(true);
    const r = await fetch(`${API}/analyze`, { method: "POST" });
    const j = await r.json();
    setContract(j.contract);
    setBusy(false);
  }
  async function loadInsights() {
    const r = await fetch(`${API}/insights`);
    const j = await r.json(); setInsights(j.insights || []);
  }
  async function loadReport(format: "md" | "html") {
    const r = await fetch(`${API}/report?format=${format}`);
    if (format === "md") setMd(await r.text());
    else setMd(""); // html показываем в iframe ниже
  }

  return (
    <div>
      <h1>AURA Analytics — Dashboard</h1>
      <div style={{display:"flex", gap:12, flexWrap:"wrap", margin:"12px 0"}}>
        <button onClick={ingestSample} disabled={busy}>Load sample</button>
        <label style={{border:"1px solid #ccc", padding:"6px 10px", cursor:"pointer"}}>
          Upload CSV/JSON
          <input type="file" style={{display:"none"}} onChange={e=>e.target.files && uploadFile(e.target.files[0])}/>
        </label>
        <button onClick={analyze} disabled={busy}>Analyze</button>
        <button onClick={loadInsights}>Insights</button>
        <button onClick={()=>loadReport("md")}>Report (MD)</button>
        <button onClick={()=>loadReport("html")}>Report (HTML)</button>
      </div>

      {contract && (
        <div style={{border:"1px solid #eee", padding:12, margin:"12px 0"}}>
          <b>Contract:</b> {contract.ok ? "OK ✅" : "Issues ⚠️"}
          {!contract.ok && (
            <ul>
              {contract.missing?.map((m:string)=><li key={m}>Missing: {m}</li>)}
              {contract.any_of_missing?.map((m:any,idx:number)=>
                <li key={idx}>One of required: {Object.values(m).join(", ")}</li>)}
            </ul>
          )}
        </div>
      )}

      {!!insights.length && (
        <div style={{border:"1px solid #eee", padding:12, margin:"12px 0"}}>
          <h3>Insights</h3>
          <ul>
          {insights.map((i:any)=>(
            <li key={i.id}><b>{i.title}</b> — {i.summary}</li>
          ))}
          </ul>
        </div>
      )}

      {md && (
        <div style={{border:"1px solid #eee", padding:12, margin:"12px 0"}}>
          <h3>Report (Markdown)</h3>
          <div dangerouslySetInnerHTML={{__html: marked(md)}} />
        </div>
      )}

      {!md && (
        <iframe title="HTML report" src={`${API}/report?format=html`} style={{width:"100%", height:600, border:"1px solid #eee"}} />
      )}
    </div>
  );
}
