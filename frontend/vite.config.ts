import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import faroUploader from "@grafana/faro-rollup-plugin";
import { loadEnv } from "vite";
import { type ViteDevServer } from 'vite'

import { Server } from 'socket.io'

const webSocketServer = {
	name: 'webSocketServer',
	configureServer(server: ViteDevServer) {
		if (!server.httpServer) return

		const io = new Server(server.httpServer)

		io.on('connection', (socket) => {
			socket.emit('eventFromServer', 'Hello, World 👋')
		})
	}
}

export default defineConfig(({ mode }) => {

  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      sveltekit(),
      webSocketServer
    ],
    test: {
      include: ["src/**/*.{test,spec}.{js,ts}"],
    },
    build: {
      sourcemap: true, // Config vite to generate sourcemap when bundling.
    },
  }
});
