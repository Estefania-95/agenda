const API_BASE_URL = 'http://localhost:8000';

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || response.statusText);
  }

  return response.json();
}

export const agendaApi = {
  getPersonas: (q?: string) => fetchApi(`/personas${q ? `?q=${q}` : ''}`),
  getStats: () => fetchApi('/stats'),
  deletePersona: (id: number) => fetchApi(`/personas/${id}`, { method: 'DELETE' }),
  createPersona: (data: any) => fetchApi('/personas', { method: 'POST', body: JSON.stringify(data) }),
};
