async function parse(res: Response) {
  const text = await res.text()
  let json: unknown = null
  try {
    json = text ? JSON.parse(text) : null
  } catch {
    json = { message: text }
  }
  if (!res.ok) {
    const msg =
      json && typeof json === 'object' && 'message' in json
        ? String((json as { message: unknown }).message)
        : `HTTP ${res.status}`
    throw new Error(msg)
  }
  return json
}

export const api = {
  get: (url: string) => fetch(url).then(parse),
  postJson: (url: string, body: unknown) =>
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(parse),
  putJson: (url: string, body: unknown) =>
    fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(parse),
  postForm: (url: string, body: FormData) =>
    fetch(url, { method: 'POST', body }).then(parse),
}
