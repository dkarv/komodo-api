import { Section } from "@components/layouts";
import { Log, LogSection } from "@components/log";
import { useRead } from "@lib/hooks";
import { Types } from "komodo_client";
import { ReactNode } from "react";

export const ContainerLogs = ({
  id,
  container_name,
  titleOther,
  disabled,
}: {
  id: string;
  container_name: string;
  titleOther?: ReactNode;
  disabled: boolean;
}) => {
  if (disabled) {
    return (
      <Section titleOther={titleOther}>
        <h1>Logs are disabled.</h1>
      </Section>
    );
  }
  return (
    <LogSection
      titleOther={titleOther}
      regular_logs={(timestamps, stream, tail, poll) =>
        NoSearchLogs(id, container_name, tail, timestamps, stream, poll)
      }
      search_logs={(timestamps, terms, invert, poll) =>
        SearchLogs(id, container_name, terms, invert, timestamps, poll)
      }
    />
  );
};

const NoSearchLogs = (
  id: string,
  container: string,
  tail: number,
  timestamps: boolean,
  stream: string,
  poll: boolean
) => {
  const { data: log, refetch } = useRead(
    "GetContainerLog",
    {
      server: id,
      container,
      tail: Number(tail),
      timestamps,
    },
    { refetchInterval: poll ? 3000 : false }
  );
  return {
    Log: (
      <div className="relative">
        <Log log={log} stream={stream as "stdout" | "stderr"} />
      </div>
    ),
    refetch,
    stderr: !!log?.stderr,
  };
};

const SearchLogs = (
  id: string,
  container: string,
  terms: string[],
  invert: boolean,
  timestamps: boolean,
  poll: boolean
) => {
  const { data: log, refetch } = useRead(
    "SearchContainerLog",
    {
      server: id,
      container,
      terms,
      combinator: Types.SearchCombinator.And,
      invert,
      timestamps,
    },
    { refetchInterval: poll ? 10000 : false }
  );
  return {
    Log: (
      <div className="h-full relative">
        <Log log={log} stream="stdout" />
      </div>
    ),
    refetch,
    stderr: !!log?.stderr,
  };
};
