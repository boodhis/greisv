// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://boodhis.github.io/greisv/',
	integrations: [
		starlight({
			title: 'Цифровая Крепость',
			logo: { src: './src/assets/houston.webp' },
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/boodhis/greisv' },
			],
			sidebar: [
				{
					label: 'Старт',
					items: [
						{ label: 'Главная', slug: 'index' },
						{ label: 'С чего начать', slug: 'getting-started' },
						{ label: 'Установка Ubuntu', slug: 'getting-started/install-ubuntu' },
						{ label: 'Первые шаги', slug: 'getting-started/first-steps' },
						{ label: 'Загрузочная флешка', slug: 'getting-started/bootable-usb' },
					],
				},
				{
					label: 'Homelab',
					items: [
						{ label: 'Концепция', slug: 'homelab' },
						{ label: 'Железо', slug: 'homelab/hardware' },
						{ label: 'Сеть', slug: 'homelab/network' },
						{ label: 'Сервер (справочник)', slug: 'homelab/server-reference' },
					],
				},
				{
					label: 'Сервисы',
					items: [
						{ label: 'Обзор', slug: 'services' },
						{ label: 'Docker', slug: 'services/docker' },
						{ label: 'Samba', slug: 'services/samba' },
						{ label: 'MiniDLNA', slug: 'services/minidlna' },
						{ label: 'Transmission', slug: 'services/transmission' },
						{ label: 'Navidrome', slug: 'services/navidrome' },
						{ label: 'Immich', slug: 'services/immich' },
						{ label: 'SOPDS (библиотека)', slug: 'services/sopds' },
						{ label: 'MQTT / ESPHome', slug: 'services/mqtt' },
					],
				},
				{
					label: 'Гайды',
					items: [
						{ label: 'Обзор', slug: 'guides' },
						{ label: 'Диски и SMART', slug: 'guides/disk-health' },
						{ label: 'Диагностика', slug: 'guides/diagnostics' },
						{ label: 'Бекапы', slug: 'guides/backup' },
						{ label: 'SSH', slug: 'guides/ssh' },
						{ label: 'Терминал', slug: 'guides/terminal' },
						{ label: 'Wi-Fi фикс', slug: 'guides/wifi-fix' },
						{ label: 'Автосборка', slug: 'guides/auto-setup' },
						{ label: 'journalctl', slug: 'guides/journalctl' },
						{ label: 'Авто-выключение', slug: 'guides/auto-shutdown' },
					],
				},
				{
					label: 'Ресурсы',
					items: [
						{ label: 'Ссылки', slug: 'resources/links' },
						{ label: 'Git команды', slug: 'resources/git-commands' },
						{ label: 'INXI', slug: 'resources/inxi' },
						{ label: 'OpenCode на Windows', slug: 'resources/opencode-windows' },
					],
				},
				{
					label: 'Хобби',
					items: [
						{ label: 'Досуг', slug: 'hobbies' },
						{ label: 'Гитара', slug: 'hobbies/guitar' },
					],
				},
			],
			customCss: ['./src/styles/global.css'],
			head: [
				{
					tag: 'script',
					attrs: {
						src: 'https://giscus.app/widget.js',
						async: true,
						crossorigin: 'anonymous',
						'data-repo': 'boodhis/greisv',
						'data-repo-id': '',
						'data-category': 'Announcements',
						'data-category-id': '',
						'data-mapping': 'pathname',
						'data-reactions-enabled': '1',
						'data-emit-metadata': '0',
						'data-input-position': 'top',
						'data-theme': 'dark',
						'data-lang': 'ru'
					}
				}
			],
		}),
	],
});
