import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# -------------------------------------------------------------
# 1. EPISODIO 1: VENTANA 1 -> SOLO EL VIDEO SIN TITULOS
# -------------------------------------------------------------
# In buildPureSlideHTML:
old_pure_slide_fn_start = """      function buildPureSlideHTML(key) {
        const conf = PURE_SLIDE_CONFIG[key];
        if (!conf) return '';"""

new_pure_slide_fn_start = """      function buildPureSlideHTML(key) {
        const conf = PURE_SLIDE_CONFIG[key];
        if (!conf) return '';

        // Episodio 1, Ventana 1: Solo el video y nada de títulos
        if (key === 'historia-origen') {
          const nextBtn = `<button type="button" onclick="openDetailModal('historia-evolucion')" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-netflix-red hover:bg-red-700 text-white font-bold text-xs sm:text-sm transition shadow-lg ml-auto cursor-pointer"><span>Siguiente</span><i class="fa-solid fa-chevron-right text-xs"></i></button>`;
          return `
            <!-- Video Oficial sin títulos, ocupando el contenedor de forma limpia -->
            <div class="relative w-full aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl border border-white/20">
              <iframe 
                id="videoHistoriaOrigen" 
                src="https://www.youtube.com/embed/Hef7aJZxwzo?autoplay=1&mute=0&rel=0&controls=1&modestbranding=1" 
                title="Video Oficial" 
                class="w-full h-full border-0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
              </iframe>
            </div>

            <!-- Navegación a la siguiente diapositiva -->
            <div class="flex items-center justify-between pt-4 border-t border-white/10 mt-4">
              <div></div>
              ${nextBtn}
            </div>
          `;
        }"""

if old_pure_slide_fn_start in content:
    content = content.replace(old_pure_slide_fn_start, new_pure_slide_fn_start, 1)
    print("Updated buildPureSlideHTML for historia-origen")
else:
    print("WARNING: old_pure_slide_fn_start not found")

# On card 1.1:
card1_pattern = re.compile(r'<!-- Ventana 1\.1:.*?-->\s*<div class="netflix-card.*?openDetailModal\(\'historia-origen\'\).*?</div>\s*</div>\s*</div>', re.DOTALL)
new_card_1 = """<!-- Ventana 1.1: Video Oficial -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition group" onclick="openDetailModal('historia-origen')">
            <div class="relative h-44 bg-black overflow-hidden flex items-center justify-center">
              <img id="cardImgHistoriaOrigen" data-card-key="historia-origen" src="https://img.youtube.com/vi/Hef7aJZxwzo/hqdefault.jpg" alt="Video Oficial Apertura" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
              <div class="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition flex items-center justify-center">
                <div class="w-12 h-12 rounded-full bg-netflix-red/90 text-white flex items-center justify-center shadow-xl group-hover:scale-110 transition">
                  <i class="fa-solid fa-play text-sm ml-0.5"></i>
                </div>
              </div>
              <span class="absolute top-2 left-2 bg-netflix-red text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 1 • Video</span>
              <span class="absolute bottom-2 right-2 text-white/90 text-xs font-mono bg-black/70 px-1.5 py-0.5 rounded"><i class="fa-solid fa-play mr-1 text-[9px] text-netflix-red"></i> Video</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Video Oficial</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 1: Video Oficial Apertura.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-purple-300 font-semibold">Video</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>"""

if card1_pattern.search(content):
    content = card1_pattern.sub(new_card_1, content, count=1)
    print("Updated card 1.1 for historia-origen")
else:
    print("WARNING: card1_pattern not found")


# In closeDetailModal: clear modalBodyContent so YouTube video stops
old_close_modal = """        if (videoIframe) {
          videoIframe.src = '';
        }"""
new_close_modal = """        if (videoIframe) {
          videoIframe.src = '';
        }
        const bodyContentEl = document.getElementById('modalBodyContent');
        if (bodyContentEl) {
          bodyContentEl.innerHTML = '';
        }"""
if old_close_modal in content:
    content = content.replace(old_close_modal, new_close_modal, 1)
    print("Updated closeDetailModal to stop iframe playback")

# -------------------------------------------------------------
# 2. EPISODIO 4: AUDIENCIAS (7 VENTANAS)
# -------------------------------------------------------------
# Subtitle of carousel-audiencia
old_sub_4 = '<p class="text-xs sm:text-sm text-gray-400">Perfil Multigeneracional • Métricas Globales • Prosumidores y UGC • Comunidades y Fandom • Consumo Multipantalla • Fidelización de Audiencia.</p>'
new_sub_4 = '<p class="text-xs sm:text-sm text-gray-400">Audiencias • Alcance y atracción cultural • De espectadores a participantes • Dance ecene song • El trend de Tik Tok • Modelo de negocio • Domtour.</p>'
content = content.replace(old_sub_4, new_sub_4)

# Replace carousel-audiencia cards
old_carousel_audiencia_pattern = re.compile(r'<div id="carousel-audiencia".*?<!-- Fila de 6 Ventanas de Diapositivas -->\s*<div id="carousel-audiencia".*?<!-- ========================================================= -->\s*<!-- EPISODIO 5', re.DOTALL)

# Let's inspect the exact carousel-audiencia container
start_c4 = content.find('<div id="carousel-audiencia"')
end_c4 = content.find('</section>', start_c4)
if start_c4 != -1 and end_c4 != -1:
    new_carousel_audiencia_html = """<div id="carousel-audiencia" class="carousel-row flex gap-4 sm:gap-6 overflow-x-auto pb-4 pt-2 scroll-smooth">
          
          <!-- Ventana 4.1: Audiencias -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-perfil')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaPerfil" data-card-key="audiencia-perfil" src="https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=800&auto=format&fit=crop" alt="Audiencias" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-black/80 border border-purple-500/40 text-purple-300 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 1 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-perfil')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 1</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Audiencias</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 1: Audiencias.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-purple-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.2: Alcance y atracción cultural -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-metricas')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaMetricas" data-card-key="audiencia-metricas" src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=800&auto=format&fit=crop" alt="Alcance y atracción cultural" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-netflix-red text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 2 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-metricas')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 2</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Alcance y atracción cultural</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 2: Alcance y atracción cultural.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-emerald-400 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.3: De espectadores a participantes -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-prosumidores')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaProsumidores" data-card-key="audiencia-prosumidores" src="https://images.unsplash.com/photo-1579783902614-a3fb3927b675?q=80&w=800&auto=format&fit=crop" alt="De espectadores a participantes" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-purple-700 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 3 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-prosumidores')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 3</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">De espectadores a participantes</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 3: De espectadores a participantes.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-pink-400 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.4: Dance ecene song -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-fandom')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaFandom" data-card-key="audiencia-fandom" src="https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=800&auto=format&fit=crop" alt="Dance ecene song" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-blue-800 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 4 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-fandom')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 4</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Dance ecene song</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 4: Dance ecene song.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-blue-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.5: El trend de Tik Tok -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-multipantalla')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaMultipantalla" data-card-key="audiencia-multipantalla" src="https://images.unsplash.com/photo-1526738549149-8e07eca6c147?q=80&w=800&auto=format&fit=crop" alt="El trend de Tik Tok" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-amber-700 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 5 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-multipantalla')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 5</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">El trend de Tik Tok</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 5: El trend de Tik Tok.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-amber-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.6: Modelo de negocio -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-fidelizacion')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaFidelizacion" data-card-key="audiencia-fidelizacion" src="https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=800&auto=format&fit=crop" alt="Modelo de negocio" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-teal-800 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 6 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-fidelizacion')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 6</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Modelo de negocio</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 6: Modelo de negocio.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-teal-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 4.7: Domtour -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('audiencia-domtour')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgAudienciaDomtour" data-card-key="audiencia-domtour" src="https://images.unsplash.com/photo-1513694203232-719a280e022f?q=80&w=800&auto=format&fit=crop" alt="Domtour" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-indigo-800 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 7 • Diapositiva</span>
              <label class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-black/80 hover:bg-netflix-red text-white flex items-center justify-center cursor-pointer transition shadow-lg border border-white/20" title="Subir imagen" onclick="event.stopPropagation();"><i class="fa-solid fa-camera text-[10px]"></i><input type="file" accept="image/*" class="hidden" onchange="handleQuickCardImageUpload(event, 'audiencia-domtour')" /></label>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 7</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Domtour</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 7: Domtour.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-indigo-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-300">Reproducir <i class="fa-solid fa-play text-[9px] text-netflix-red"></i></span>
              </div>
            </div>
          </div>

        </div>"""
    content = content[:start_c4] + new_carousel_audiencia_html + content[end_c4:]
    print("Updated carousel-audiencia cards for Episodio 4 (all 7 windows)")

# -------------------------------------------------------------
# 3. EPISODIO 5: ESTRUCTURA (5 VENTANAS)
# -------------------------------------------------------------
old_sub_5 = '<p class="text-xs sm:text-sm text-gray-400">Inicio de la Transmediación • Franquicia o Experiencia Transmedia • Principios de Jenkins • Canon y Lore • Matriz Didáctica.</p>'
new_sub_5 = '<p class="text-xs sm:text-sm text-gray-400">Inicio de Transmediación • Franquicia o Esperiencia transmedia • ¿Existe un final? • ¿Cómo está estructurado el proyecto? • Uso de la tecnología.</p>'
content = content.replace(old_sub_5, new_sub_5)

start_c5 = content.find('<div id="carousel-estructura"')
end_c5 = content.find('</section>', start_c5)
if start_c5 != -1 and end_c5 != -1:
    new_carousel_estructura_html = """<div id="carousel-estructura" class="carousel-row flex gap-4 sm:gap-6 overflow-x-auto pb-4 pt-2 scroll-smooth">
          
          <!-- Ventana 5.1: Inicio de Transmediación -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('estructura-canales')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgEstructuraCanales" data-card-key="estructura-canales" src="/user_drive_exact.png" alt="Inicio de Transmediación" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-netflix-red text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 1 • Diapositiva</span>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 1</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Inicio de Transmediación</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 1: Inicio de Transmediación.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-purple-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-400">Abrir <i class="fa-solid fa-arrow-right text-[10px]"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 5.2: Franquicia o Esperiencia transmedia -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('estructura-diagrama')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgEstructuraDiagrama" data-card-key="estructura-diagrama" src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=800&auto=format&fit=crop" alt="Franquicia o Esperiencia transmedia" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-black/80 border border-purple-500/40 text-purple-300 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 2 • Diapositiva</span>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 2</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Franquicia o Esperiencia transmedia</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 2: Franquicia o Esperiencia transmedia.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-purple-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-400">Abrir <i class="fa-solid fa-arrow-right text-[10px]"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 5.3: ¿Existe un final? -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('estructura-jenkins')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgEstructuraJenkins" data-card-key="estructura-jenkins" src="https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=800&auto=format&fit=crop" alt="¿Existe un final?" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-purple-800 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 3 • Diapositiva</span>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 3</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">¿Existe un final?</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 3: ¿Existe un final?.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-amber-400 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-400">Abrir <i class="fa-solid fa-arrow-right text-[10px]"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 5.4: ¿Cómo está estructurado el proyecto? -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('estructura-canon')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgEstructuraCanon" data-card-key="estructura-canon" src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800&auto=format&fit=crop" alt="¿Cómo está estructurado el proyecto?" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-blue-900 text-blue-200 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 4 • Diapositiva</span>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 4</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">¿Cómo está estructurado el proyecto?</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 4: ¿Cómo está estructurado el proyecto?.</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-blue-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-400">Abrir <i class="fa-solid fa-arrow-right text-[10px]"></i></span>
              </div>
            </div>
          </div>

          <!-- Ventana 5.5: Uso de la tecnología. -->
          <div class="netflix-card flex-none w-[280px] sm:w-[320px] bg-netflix-card rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-netflix-red transition" onclick="openDetailModal('estructura-evaluacion')">
            <div class="relative h-44 bg-zinc-900 overflow-hidden flex items-center justify-center">
              <img id="cardImgEstructuraEvaluacion" data-card-key="estructura-evaluacion" src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800&auto=format&fit=crop" alt="Uso de la tecnología." class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-netflix-card via-black/40 to-transparent"></div>
              <span class="absolute top-2 left-2 bg-emerald-900 text-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Ventana 5 • Diapositiva</span>
              <span class="absolute bottom-2 right-2 text-white/80 text-xs font-mono"><i class="fa-solid fa-clone mr-1"></i> Diapo 5</span>
            </div>
            <div class="p-4 space-y-2">
              <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition">Uso de la tecnología.</h3>
              <p class="text-xs text-gray-400 line-clamp-1">Ventana 5: Uso de la tecnología..</p>
              <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs text-gray-400">
                <span class="text-emerald-300 font-semibold">Diapositiva</span>
                <span class="hover:text-white flex items-center gap-1 font-medium text-purple-400">Abrir <i class="fa-solid fa-arrow-right text-[10px]"></i></span>
              </div>
            </div>
          </div>

        </div>"""
    content = content[:start_c5] + new_carousel_estructura_html + content[end_c5:]
    print("Updated carousel-estructura cards for Episodio 5 (all 5 windows)")

# -------------------------------------------------------------
# 4. ACTUALIZAR transmediaData Y PURE_SLIDE_CONFIG
# -------------------------------------------------------------
# In transmediaData for Episodio 4:
old_tm_ep4_pattern = re.compile(r"// EPISODIO 4: AUDIENCIA \(6 Ventanas\).*?// EPISODIO 5: ESTRUCTURA", re.DOTALL)
new_tm_ep4 = """// EPISODIO 4: AUDIENCIA (7 Ventanas)
        'audiencia-perfil': {
          title: 'Audiencias',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 1',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-perfil')
        },
        'audiencia-metricas': {
          title: 'Alcance y atracción cultural',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 2',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-metricas')
        },
        'audiencia-prosumidores': {
          title: 'De espectadores a participantes',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 3',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-prosumidores')
        },
        'audiencia-fandom': {
          title: 'Dance ecene song',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 4',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-fandom')
        },
        'audiencia-multipantalla': {
          title: 'El trend de Tik Tok',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 5',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-multipantalla')
        },
        'audiencia-fidelizacion': {
          title: 'Modelo de negocio',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 6',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-fidelizacion')
        },
        'audiencia-domtour': {
          title: 'Domtour',
          category: 'EPISODIO 4: AUDIENCIA',
          date: 'Ventana 7',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('audiencia-domtour')
        },

        // EPISODIO 5: ESTRUCTURA"""

if old_tm_ep4_pattern.search(content):
    content = old_tm_ep4_pattern.sub(new_tm_ep4, content, count=1)
    print("Updated transmediaData for Episodio 4 (all 7 titles)")

# In transmediaData for Episodio 5:
old_tm_ep5_pattern = re.compile(r"// EPISODIO 5: ESTRUCTURA \(5 Ventanas\).*?content: \(\) => buildPureSlideHTML\('estructura-evaluacion'\)\s*\}", re.DOTALL)
new_tm_ep5 = """// EPISODIO 5: ESTRUCTURA (5 Ventanas)
        'estructura-canales': {
          title: 'Inicio de Transmediación',
          category: 'EPISODIO 5: ESTRUCTURA',
          date: 'Ventana 1',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('estructura-canales')
        },
        'estructura-diagrama': {
          title: 'Franquicia o Esperiencia transmedia',
          category: 'EPISODIO 5: ESTRUCTURA',
          date: 'Ventana 2',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('estructura-diagrama')
        },
        'estructura-jenkins': {
          title: '¿Existe un final?',
          category: 'EPISODIO 5: ESTRUCTURA',
          date: 'Ventana 3',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('estructura-jenkins')
        },
        'estructura-canon': {
          title: '¿Cómo está estructurado el proyecto?',
          category: 'EPISODIO 5: ESTRUCTURA',
          date: 'Ventana 4',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('estructura-canon')
        },
        'estructura-evaluacion': {
          title: 'Uso de la tecnología.',
          category: 'EPISODIO 5: ESTRUCTURA',
          date: 'Ventana 5',
          type: 'Diapositiva',
          isPureSlide: true,
          content: () => buildPureSlideHTML('estructura-evaluacion')
        }"""

if old_tm_ep5_pattern.search(content):
    content = old_tm_ep5_pattern.sub(new_tm_ep5, content, count=1)
    print("Updated transmediaData for Episodio 5 (all 5 titles)")

# In PURE_SLIDE_CONFIG for Episodio 4 and 5:
old_cfg_ep4_5_pattern = re.compile(r"// EPISODIO 4: AUDIENCIA \(6 Ventanas\).*?'estructura-evaluacion': \{.*?'title': 'MATRIZ DIDÁCTICA DEL ECOSISTEMA',.*?nextKey: null\s*\}", re.DOTALL)
new_cfg_ep4_5 = """// EPISODIO 4: AUDIENCIA (7 Ventanas)
        'audiencia-perfil': {
          storageKey: 'custom_audiencia_perfil_img',
          targetImgId: 'imgAudienciaPerfil',
          cardImgId: 'cardImgAudienciaPerfil',
          title: 'AUDIENCIAS',
          defaultImg: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=1200&auto=format&fit=crop',
          prevKey: null,
          nextKey: 'audiencia-metricas'
        },
        'audiencia-metricas': {
          storageKey: 'custom_audiencia_metricas_img',
          targetImgId: 'imgAudienciaMetricas',
          cardImgId: 'cardImgAudienciaMetricas',
          title: 'ALCANCE Y ATRACCIÓN CULTURAL',
          defaultImg: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-perfil',
          nextKey: 'audiencia-prosumidores'
        },
        'audiencia-prosumidores': {
          storageKey: 'custom_audiencia_prosumidores_img',
          targetImgId: 'imgAudienciaProsumidores',
          cardImgId: 'cardImgAudienciaProsumidores',
          title: 'DE ESPECTADORES A PARTICIPANTES',
          defaultImg: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-metricas',
          nextKey: 'audiencia-fandom'
        },
        'audiencia-fandom': {
          storageKey: 'custom_audiencia_fandom_img',
          targetImgId: 'imgAudienciaFandom',
          cardImgId: 'cardImgAudienciaFandom',
          title: 'DANCE ECENE SONG',
          defaultImg: 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-prosumidores',
          nextKey: 'audiencia-multipantalla'
        },
        'audiencia-multipantalla': {
          storageKey: 'custom_audiencia_multipantalla_img',
          targetImgId: 'imgAudienciaMultipantalla',
          cardImgId: 'cardImgAudienciaMultipantalla',
          title: 'EL TREND DE TIK TOK',
          defaultImg: 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-fandom',
          nextKey: 'audiencia-fidelizacion'
        },
        'audiencia-fidelizacion': {
          storageKey: 'custom_audiencia_fidelizacion_img',
          targetImgId: 'imgAudienciaFidelizacion',
          cardImgId: 'cardImgAudienciaFidelizacion',
          title: 'MODELO DE NEGOCIO',
          defaultImg: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-multipantalla',
          nextKey: 'audiencia-domtour'
        },
        'audiencia-domtour': {
          storageKey: 'custom_audiencia_domtour_img',
          targetImgId: 'imgAudienciaDomtour',
          cardImgId: 'cardImgAudienciaDomtour',
          title: 'DOMTOUR',
          defaultImg: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'audiencia-fidelizacion',
          nextKey: 'estructura-canales'
        },

        // EPISODIO 5: ESTRUCTURA (5 Ventanas)
        'estructura-canales': {
          storageKey: 'custom_user_drive_exact_img',
          targetImgId: 'imgUserDriveExact',
          cardImgId: 'cardImgEstructuraCanales',
          title: 'INICIO DE TRANSMEDIACIÓN',
          defaultImg: '/user_drive_exact.png',
          prevKey: 'audiencia-domtour',
          nextKey: 'estructura-diagrama'
        },
        'estructura-diagrama': {
          storageKey: 'custom_estructura_diagrama_img',
          targetImgId: 'imgEstructuraDiagrama',
          cardImgId: 'cardImgEstructuraDiagrama',
          title: 'FRANQUICIA O ESPERIENCIA TRANSMEDIA',
          defaultImg: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'estructura-canales',
          nextKey: 'estructura-jenkins'
        },
        'estructura-jenkins': {
          storageKey: 'custom_estructura_jenkins_img',
          targetImgId: 'imgEstructuraJenkins',
          cardImgId: 'cardImgEstructuraJenkins',
          title: '¿EXISTE UN FINAL?',
          defaultImg: 'https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'estructura-diagrama',
          nextKey: 'estructura-canon'
        },
        'estructura-canon': {
          storageKey: 'custom_estructura_canon_img',
          targetImgId: 'imgEstructuraCanon',
          cardImgId: 'cardImgEstructuraCanon',
          title: '¿CÓMO ESTÁ ESTRUCTURADO EL PROYECTO?',
          defaultImg: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'estructura-jenkins',
          nextKey: 'estructura-evaluacion'
        },
        'estructura-evaluacion': {
          storageKey: 'custom_estructura_evaluacion_img',
          targetImgId: 'imgEstructuraEvaluacion',
          cardImgId: 'cardImgEstructuraEvaluacion',
          title: 'USO DE LA TECNOLOGÍA.',
          defaultImg: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1200&auto=format&fit=crop',
          prevKey: 'estructura-canon',
          nextKey: null
        }"""

if old_cfg_ep4_5_pattern.search(content):
    content = old_cfg_ep4_5_pattern.sub(new_cfg_ep4_5, content, count=1)
    print("Updated PURE_SLIDE_CONFIG for Episodios 4 and 5")
else:
    print("WARNING: old_cfg_ep4_5_pattern not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html update complete!")
