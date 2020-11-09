const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

export interface URLParameters {
  path: string;
  resourceId?: string;
  query?: string;
}
const constructUrl = ({ path, resourceId, query }: URLParameters) => {
  if (!path) {
    throw new Error('Path is required');
  }

  const basePath = apiBase! + path;

  let url = basePath;
  url = resourceId ? url + '/' + resourceId : url;
  url = query ? url + '?' + query : url;

  return url;
};

export default constructUrl;
