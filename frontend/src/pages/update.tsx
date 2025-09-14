import { UpdateDetailsInner } from "@components/updates/details";
import { useRead, useSetTitle } from "@lib/hooks";
import { To, useLocation, useNavigate, useParams } from "react-router-dom";

export default function UpdatePage() {
  useSetTitle("Update");
  // https://github.com/remix-run/react-router/discussions/9788#discussioncomment-4604278
  const navTo = (useLocation().key === "default" ? "/" : -1) as To;
  const navigate = useNavigate();
  const id = useParams().id as string;
  const update = useRead("GetUpdate", { id }).data;

  if (!update) return null;

  return <UpdateDetailsInner id={id} open setOpen={() => navigate(navTo)} />;
}
