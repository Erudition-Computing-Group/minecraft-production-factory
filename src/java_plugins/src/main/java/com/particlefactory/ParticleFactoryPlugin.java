package com.particlefactory;

import com.particlefactory.emitters.BurstEmitter;
import com.particlefactory.emitters.Emitter;
import com.particlefactory.emitters.GoldenTreasureEmitter;
import com.particlefactory.emitters.OrbitEmitter;
import com.particlefactory.math.Particle;
import com.particlefactory.math.Vec3;
import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.Particle.DustOptions;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.scheduler.BukkitTask;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * ParticleFactoryPlugin — main entry point.
 * Manages active emitters and renders them each tick using PaperMC's particle API.
 */
public class ParticleFactoryPlugin extends JavaPlugin {

    private final Map<UUID, List<Emitter>> activeEmitters = new HashMap<>();
    private BukkitTask tickTask;

    @Override
    public void onEnable() {
        getLogger().info("ParticleFactory enabled!");

        // Tick all emitters every 1 tick (50ms)
        tickTask = new BukkitRunnable() {
            @Override
            public void run() {
                for (Map.Entry<UUID, List<Emitter>> entry : activeEmitters.entrySet()) {
                    Player player = Bukkit.getPlayer(entry.getKey());
                    if (player == null || !player.isOnline()) continue;
                    for (Emitter em : entry.getValue()) {
                        em.update(1.0);
                        renderEmitter(player, em);
                    }
                }
            }
        }.runTaskTimer(this, 0L, 1L);
    }

    @Override
    public void onDisable() {
        if (tickTask != null) tickTask.cancel();
        activeEmitters.clear();
        getLogger().info("ParticleFactory disabled.");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("Players only.");
            return true;
        }
        Player player = (Player) sender;
        UUID uuid = player.getUniqueId();

        if (args.length == 0) {
            player.sendMessage("Usage: /cosmetics [burst|orbit|treasure|clear]");
            return true;
        }

        switch (args[0].toLowerCase()) {
            case "burst":
                List<Emitter> list = activeEmitters.computeIfAbsent(uuid, k -> new ArrayList<>());
                Vec3 pos = new Vec3(player.getLocation().getX(), player.getLocation().getY() + 1, player.getLocation().getZ());
                BurstEmitter burst = new BurstEmitter(pos, 20, 0.8, 20, 0.15, 1.0, 0.6, 0.1);
                burst.spawn();
                list.add(burst);
                player.sendMessage("Burst effect activated!");
                break;
            case "orbit":
                List<Emitter> list2 = activeEmitters.computeIfAbsent(uuid, k -> new ArrayList<>());
                Vec3 pos2 = new Vec3(player.getLocation().getX(), player.getLocation().getY() + 2, player.getLocation().getZ());
                OrbitEmitter orbit = new OrbitEmitter(pos2, 12, 0.8, 0.3, 0.15, 40, 0.08, 1.0, 0.9, 0.3);
                list2.add(orbit);
                player.sendMessage("Orbit effect activated!");
                break;
            case "treasure":
                List<Emitter> treasureEmitters = activeEmitters.computeIfAbsent(uuid, k -> new ArrayList<>());
                Location treasureLocation = player.getLocation();
                treasureEmitters.add(new GoldenTreasureEmitter(
                    new Vec3(treasureLocation.getX(), treasureLocation.getY() + 0.8, treasureLocation.getZ())
                ));
                player.sendMessage("Golden Treasure sparkle activated for 10 seconds!");
                break;
            case "clear":
                activeEmitters.remove(uuid);
                player.sendMessage("All effects cleared.");
                break;
            default:
                player.sendMessage("Unknown: " + args[0]);
        }
        return true;
    }

    /** Render an emitter's particles using PaperMC particle API. */
    private void renderEmitter(Player viewer, Emitter em) {
        Location base = viewer.getLocation();
        for (Particle p : em.getParticles()) {
            if (p.pos.distanceTo(new Vec3(base.getX(), base.getY(), base.getZ())) > 32) continue;
            Location loc = new Location(viewer.getWorld(), p.pos.x, p.pos.y, p.pos.z);
            DustOptions dust = new DustOptions(
                Color.fromRGB((int)(p.r * 255), (int)(p.g * 255), (int)(p.b * 255)),
                (float) p.size
            );
            viewer.spawnParticle(org.bukkit.Particle.DUST, loc, 1, 0, 0, 0, 0, dust);
        }
    }
}
