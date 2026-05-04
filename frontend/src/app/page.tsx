'use client';

import { useEffect, useState } from 'react';
import { agendaApi, fetchApi } from '@/lib/api';
import styles from './page.module.css';

type View = 'listar' | 'nuevo' | 'buscar' | 'reportes' | 'editar';

export default function Home() {
  const [view, setView] = useState<View>('listar');
  const [personas, setPersonas] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [formData, setFormData] = useState({ nombre: '', apellido: '', cuil: '' });
  const [editingId, setEditingId] = useState<number | null>(null);

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

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await agendaApi.createPersona(formData);
      setFormData({ nombre: '', apellido: '', cuil: '' });
      setView('listar');
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleEditClick = (persona: any) => {
    setEditingId(persona.id);
    setFormData({ nombre: persona.nombre, apellido: persona.apellido, cuil: persona.cuil });
    setView('editar');
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingId) return;
    try {
      await fetchApi(`/personas/${editingId}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      setEditingId(null);
      setFormData({ nombre: '', apellido: '', cuil: '' });
      setView('listar');
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('¿Está seguro de eliminar este registro?')) {
      try {
        await agendaApi.deletePersona(id);
        loadData();
      } catch (err: any) {
        alert(err.message);
      }
    }
  };

  return (
    <div className={styles.container}>
      {/* Sidebar Menu */}
      <aside className={`${styles.sidebar} glass`}>
        <div className={styles.logo}>
          <h2 className="gradient-text">AGENDA</h2>
          <span>v1.0 Modular</span>
        </div>
        <nav className={styles.nav}>
          <button onClick={() => setView('listar')} className={view === 'listar' ? styles.active : ''}>
            <i>📋</i> Listar
          </button>
          <button onClick={() => setView('nuevo')} className={view === 'nuevo' ? styles.active : ''}>
            <i>➕</i> Nuevo
          </button>
          <button onClick={() => setView('buscar')} className={view === 'buscar' ? styles.active : ''}>
            <i>🔍</i> Buscar
          </button>
          <button onClick={() => setView('reportes')} className={view === 'reportes' ? styles.active : ''}>
            <i>📊</i> Reportes
          </button>
        </nav>
      </aside>

      <main className={styles.mainContent}>
        <header className={styles.header}>
          <h1 className="gradient-text">
            {view === 'listar' && 'Listado de Personas'}
            {view === 'nuevo' && 'Nueva Persona'}
            {view === 'buscar' && 'Búsqueda Avanzada'}
            {view === 'reportes' && 'Reportes Estadísticos'}
          </h1>
          <div className={styles.headerStats}>
            <div className="glass card">
              <span className={styles.statLabel}>Total</span>
              <span className={styles.statValueSmall}>{stats?.total || 0}</span>
            </div>
          </div>
        </header>

        <section className={styles.content}>
          {view === 'listar' && (
            <div className="glass animate-fade-in">
              <div className={styles.tableWrapper}>
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nombre</th>
                      <th>CUIL</th>
                      <th>Fecha</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {loading ? (
                      <tr><td colSpan={5} className={styles.centered}>Cargando...</td></tr>
                    ) : personas.map(p => (
                      <tr key={p.id}>
                        <td>#{p.id}</td>
                        <td><span className={styles.name}>{p.nombre} {p.apellido}</span></td>
                        <td><code className={styles.cuil}>{p.cuil}</code></td>
                        <td>{new Date(p.fecha_registro).toLocaleDateString()}</td>
                        <td>
                          <div className={styles.actions}>
                            <button onClick={() => handleEditClick(p)} className={styles.btnEdit}>Editar</button>
                            <button onClick={() => handleDelete(p.id)} className={styles.btnDelete}>Baja</button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {view === 'nuevo' && (
            <div className="glass animate-fade-in" style={{ padding: '2rem', maxWidth: '600px' }}>
              <form onSubmit={handleCreate} className={styles.form}>
                <div className={styles.inputGroup}>
                  <label>Nombre</label>
                  <input 
                    required 
                    minLength={2}
                    placeholder="Ej: Juan"
                    value={formData.nombre} 
                    onChange={e => setFormData({...formData, nombre: e.target.value})} 
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label>Apellido</label>
                  <input 
                    required 
                    minLength={2}
                    placeholder="Ej: Pérez"
                    value={formData.apellido} 
                    onChange={e => setFormData({...formData, apellido: e.target.value})} 
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label>CUIL</label>
                  <input 
                    placeholder="20-12345678-9" 
                    required 
                    pattern="\d{2}-\d{8}-\d{1}"
                    title="Formato esperado: XX-XXXXXXXX-X"
                    value={formData.cuil} 
                    onChange={e => setFormData({...formData, cuil: e.target.value})} 
                  />
                  <small style={{ color: 'rgba(255,255,255,0.4)', marginTop: '0.25rem' }}>
                    Formato: XX-XXXXXXXX-X (con guiones)
                  </small>
                </div>
                <button type="submit" className={styles.searchButton} style={{ width: '100%', marginTop: '1rem' }}>
                  Guardar Persona
                </button>
              </form>
            </div>
          )}

          {view === 'editar' && (
            <div className="glass animate-fade-in" style={{ padding: '2rem', maxWidth: '600px' }}>
              <form onSubmit={handleUpdate} className={styles.form}>
                <div className={styles.inputGroup}>
                  <label>Nombre</label>
                  <input 
                    required 
                    minLength={2}
                    placeholder="Ej: Juan"
                    value={formData.nombre} 
                    onChange={e => setFormData({...formData, nombre: e.target.value})} 
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label>Apellido</label>
                  <input 
                    required 
                    minLength={2}
                    placeholder="Ej: Pérez"
                    value={formData.apellido} 
                    onChange={e => setFormData({...formData, apellido: e.target.value})} 
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label>CUIL</label>
                  <input 
                    placeholder="20-12345678-9" 
                    required 
                    pattern="\d{2}-\d{8}-\d{1}"
                    title="Formato esperado: XX-XXXXXXXX-X"
                    value={formData.cuil} 
                    onChange={e => setFormData({...formData, cuil: e.target.value})} 
                  />
                </div>
                <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                  <button type="submit" className={styles.searchButton} style={{ flex: 1 }}>
                    Actualizar Datos
                  </button>
                  <button type="button" onClick={() => setView('listar')} className={styles.btnDelete} style={{ flex: 1 }}>
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          )}

          {view === 'buscar' && (
            <div className="animate-fade-in">
              <form onSubmit={(e) => { e.preventDefault(); loadData(search); }} className="glass" style={{ display: 'flex', padding: '1rem', marginBottom: '2rem', gap: '1rem' }}>
                <input 
                  type="text" 
                  placeholder="Buscar por nombre, apellido o CUIL..." 
                  className={styles.searchInput}
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                />
                <button type="submit" className={styles.searchButton}>Buscar</button>
              </form>
              <div className="glass">
                {/* Same table as list but filtered */}
                <div className={styles.tableWrapper}>
                  <table className={styles.table}>
                    {/* ... (same table body as listar) */}
                    <tbody>
                      {personas.map(p => (
                        <tr key={p.id}>
                          <td>#{p.id}</td>
                          <td><span className={styles.name}>{p.nombre} {p.apellido}</span></td>
                          <td><code className={styles.cuil}>{p.cuil}</code></td>
                          <td>{new Date(p.fecha_registro).toLocaleDateString()}</td>
                          <td>
                            <div className={styles.actions}>
                              <button onClick={() => handleDelete(p.id)} className={styles.btnDelete}>Baja</button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {view === 'reportes' && (
            <div className="animate-fade-in">
              <div className={styles.statsGrid}>
                <div className="glass card">
                  <h3>Estadísticas Generales</h3>
                  <div style={{ marginTop: '1rem' }}>
                    <p>Total de personas: <strong>{stats?.total || 0}</strong></p>
                    <p>Primer Registro: <strong>
                      {stats?.primer_registro 
                        ? `${stats.primer_registro.nombre} ${stats.primer_registro.apellido}` 
                        : 'N/A'}
                    </strong></p>
                    <p>Último Registro: <strong>
                      {stats?.ultimo_registro 
                        ? `${stats.ultimo_registro.nombre} ${stats.ultimo_registro.apellido}` 
                        : 'N/A'}
                    </strong></p>
                  </div>
                </div>
                <div className="glass card">
                  <h3>Formatos de Exportación</h3>
                  <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                    <button className={styles.btnEdit}>CSV</button>
                    <button className={styles.btnEdit}>XLSX</button>
                    <button className={styles.btnEdit}>PDF</button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
