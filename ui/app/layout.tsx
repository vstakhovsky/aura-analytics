export const metadata = { title: "AURA Analytics", description: "MVP Dashboard" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body style={{fontFamily:"system-ui, -apple-system, Segoe UI, Roboto, Arial"}}>
    <div style={{maxWidth:960, margin:"32px auto"}}>{children}</div></body></html>);
}
