const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
    }

    return response.json();
  } catch (err) {
    console.error(`Fetch error on ${url}:`, err);
    throw err;
  }
}

export const agendaApi = {
  getPersonas: (q?: string) => fetchApi(`/personas${q ? `?q=${q}` : ''}`),
  getStats: () => fetchApi('/stats'),
  deletePersona: (id: number) => fetchApi(`/personas/${id}`, { method: 'DELETE' }),
  createPersona: (data: any) => fetchApi('/personas', { method: 'POST', body: JSON.stringify(data) }),
};
