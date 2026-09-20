import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: NextRequest) {
  try {
    const configPath = path.join(process.cwd(), 'public', 'network_config.json');
    if (fs.existsSync(configPath)) {
      const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return NextResponse.json(data);
    }
  } catch (err) {
    console.error('Error reading network_config.json:', err);
  }

  // Fallback to host header if not localhost
  const host = request.headers.get('host') || '10.129.251.37:3000';
  const ip = host.split(':')[0];
  const port = host.split(':')[1] || '3000';
  return NextResponse.json({
    ip: (ip !== 'localhost' && ip !== '127.0.0.1') ? ip : '10.129.251.37',
    port,
    url: `http://${(ip !== 'localhost' && ip !== '127.0.0.1') ? ip : '10.129.251.37'}:${port}`
  });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const rawIp = body.ip || '';
    const cleanIp = rawIp.trim().replace(/^https?:\/\//, '').split(':')[0].split('/')[0];
    
    if (!cleanIp) {
      return NextResponse.json({ error: 'Valid IP address required' }, { status: 400 });
    }

    const payload = {
      ip: cleanIp,
      port: '3000',
      url: `http://${cleanIp}:3000`
    };

    const configPath = path.join(process.cwd(), 'public', 'network_config.json');
    fs.writeFileSync(configPath, JSON.stringify(payload, null, 2), 'utf8');

    // Also update backend config if accessible
    try {
      const backendConfig = path.join(process.cwd(), '..', 'backend', 'network_config.json');
      if (fs.existsSync(path.dirname(backendConfig))) {
        fs.writeFileSync(backendConfig, JSON.stringify(payload, null, 2), 'utf8');
      }
    } catch {}

    return NextResponse.json(payload);
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Failed to update network IP' }, { status: 500 });
  }
}
