'use client';

import { useEffect, useState } from 'react';
import { agendaApi } from '@/lib/api';
import styles from './page.module.css';

export default function Home() {
  const [personas, setPersonas] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (query?: string) => {
    try {
      setLoading(true);
      const [data, statsData] = await Promise.all([
        agendaApi.getPersonas(query),
        agendaApi.getStats()
      ]);
      setPersonas(data.resultados || data);
      setStats(statsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadData(search);
  };

  return (
    <main className={styles.main}>
      {/* Header Section */}
      <header className={styles.header}>
        <div>
          <h1 className="gradient-text">Sistema de Gestión</h1>
          <p className={styles.subtitle}>Panel de Control Modular | SQL Server</p>
        </div>
        <div className={styles.statsRow}>
          <div className="glass card animate-fade-in">
            <span className={styles.statLabel}>Total Registros</span>
            <span className={styles.statValue}>{stats?.total || 0}</span>
          </div>
          <div className="glass card animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <span className={styles.statLabel}>Último Registro</span>
            <span className={styles.statValueSmall}>
              {stats?.ultimo_registro ? String(stats.ultimo_registro).split(' ')[0] : 'N/A'}
            </span>
          </div>
        </div>
      </header>

      {/* Search Bar */}
      <section className={styles.searchSection}>
        <form onSubmit={handleSearch} className="glass">
          <input 
            type="text" 
            placeholder="Buscar por nombre, apellido o CUIL..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className={styles.searchInput}
          />
          <button type="submit" className={styles.searchButton}>Buscar</button>
        </form>
      </section>

      {/* Data Table */}
      <section className="glass animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre Completo</th>
                <th>CUIL</th>
                <th>Fecha Registro</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={5} className={styles.centered}>Cargando datos...</td></tr>
              ) : personas.length === 0 ? (
                <tr><td colSpan={5} className={styles.centered}>No se encontraron resultados</td></tr>
              ) : (
                personas.map((p) => (
                  <tr key={p.id}>
                    <td>#{p.id}</td>
                    <td><span className={styles.name}>{p.nombre} {p.apellido}</span></td>
                    <td><code className={styles.cuil}>{p.cuil}</code></td>
                    <td>{new Date(p.fecha_registro).toLocaleDateString()}</td>
                    <td>
                      <div className={styles.actions}>
                        <button className={styles.btnEdit}>Editar</button>
                        <button className={styles.btnDelete}>Baja</button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
