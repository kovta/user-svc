import { constructUrl } from '.';
import { RequestParameters } from './useRequest';
import fetcher from './fetcher';

const useFetch = async <T>({ path, resourceId, query }: RequestParameters) => {
  const url = constructUrl({ path, resourceId, query });

  return await fetcher<T>(url);
};

export default useFetch;
